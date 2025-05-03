(async function() {
    const selection = window.getSelection();
    const selectedText = selection ? selection.toString().trim() : '';

    const labels = await getLabelsFromServer(selectedText);

    if (labels.length === 0) {
        showTooltip(selection, 'Нет тега');
    } else {
        showTooltip(selection, `${labels.join(', ')}`);
    }
})();

async function getLabelsFromServer(text) {
    try {
// здесь будет запрос к моему серверу на Flask, который будет отдавать ответ от классификатора по API, пока что заглушка-локалхост, чтобы было
        const response = await fetch('http://localhost:8000/classify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });

        if (!response.ok) {
            console.error('Ошибка API:', response.statusText);
            return [];
        }

        const data = await response.json();
        return data.labels || [];
    } catch (error) {
        console.error('Ошибка запроса:', error);
        return [];
    }
}

function showTooltip(selection, message) {
    if (selection.rangeCount === 0) return;
    const range = selection.getRangeAt(0);
    const rect = range.getBoundingClientRect();

    const tooltip = document.createElement('div');
    tooltip.textContent = message;
    tooltip.style.position = 'absolute';
    tooltip.style.top = `${rect.top + window.scrollY - 30}px`;
    tooltip.style.left = `${rect.left + window.scrollX}px`;
    tooltip.style.backgroundColor = '#333';
    tooltip.style.color = '#fff';
    tooltip.style.padding = '5px 10px';
    tooltip.style.borderRadius = '4px';
    tooltip.style.fontSize = '14px';
    tooltip.style.zIndex = '10000';
    tooltip.style.boxShadow = '0 2px 6px rgba(0,0,0,0.2)';

    document.body.appendChild(tooltip);
}
