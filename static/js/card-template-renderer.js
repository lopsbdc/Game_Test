/**
 * Renderiza uma carta usando seu template associado
 * @param {Object} card - Dados da carta
 * @param {Object} template - Dados do template
 * @param {HTMLElement} container - Elemento onde a carta será renderizada
 * @param {Object} options - Opções de renderização (escala, modo, etc)
 */
function renderCardWithTemplate(card, template, container, options = {}) {
    // Configurações padrão
    const config = {
        scale: options.scale || 1.0,
        mode: options.mode || 'full', // full, preview, edit
        interactive: options.interactive || false
    };
    
    // Limpar container
    container.innerHTML = '';
    
    // Se não tiver template, usar visualização padrão
    if (!template || !template.zones) {
        renderDefaultCard(card, container, config);
        return;
    }
    
    // Configurar container
    container.style.position = 'relative';
    container.style.width = `${template.width_mm * 4 * config.scale}px`;
    container.style.height = `${template.height_mm * 4 * config.scale}px`;
    container.style.overflow = 'hidden';
    container.style.borderRadius = '8px';
    
    // Aplicar fundo baseado no tipo de template e cor da carta
    applyCardBackground(card, template, container);
    
    // Renderizar cada zona do template
    if (template.zones) {
        Object.entries(template.zones).forEach(([id, zone]) => {
            renderZone(id, zone, card, container, config);
        });
    }
}

/**
 * Obtém a cor CSS para uma carta baseada em seu atributo de cor
 */
function getColorForCard(card) {
    // Mapeamento de cores da carta para valores CSS
    const colorMap = {
        'Purple': 'rgba(138, 43, 226, 0.85)',
        'Blue': 'rgba(30, 144, 255, 0.85)',
        'Red': 'rgba(220, 53, 69, 0.85)',
        'Green': 'rgba(40, 167, 69, 0.85)',
        'Gold': 'rgba(255, 193, 7, 0.85)',
        // Fallback para cartas sem cor
        'default': 'rgba(108, 117, 125, 0.85)'
    };
    
    return colorMap[card.color] || colorMap.default;
}

/**
 * Aplica o fundo da carta baseado no template e na cor da carta
 */
function applyCardBackground(card, template, container) {
    // Aplicar cor baseada na carta
    container.style.backgroundColor = getColorForCard(card);
    
    // Adicionar implementação completa posteriormente
}

/**
 * Renderiza uma zona específica do template
 */
function renderZone(id, zone, card, container, config) {
    // Implementação básica inicial
    const zoneElement = document.createElement('div');
    zoneElement.className = 'template-zone';
    zoneElement.dataset.zoneId = id;
    
    // Posicionar e dimensionar a zona
    zoneElement.style.position = 'absolute';
    zoneElement.style.left = `${zone.x * config.scale}px`;
    zoneElement.style.top = `${zone.y * config.scale}px`;
    zoneElement.style.width = `${zone.width * config.scale}px`;
    zoneElement.style.height = `${zone.height * config.scale}px`;
    zoneElement.style.zIndex = zone.z_index || 1;
    
    // Adicionar borda temporária para visualização
    zoneElement.style.border = '1px dashed rgba(255, 255, 255, 0.5)';
    
    // Adicionar texto de identificação
    zoneElement.textContent = id;
    
    // Adicionar zona ao container
    container.appendChild(zoneElement);
}

/**
 * Renderiza uma carta sem template (visualização padrão/fallback)
 */
function renderDefaultCard(card, container, config) {
    // Configurar container
    container.style.position = 'relative';
    container.style.width = `${63 * 4 * config.scale}px`; // Largura padrão
    container.style.height = `${88 * 4 * config.scale}px`; // Altura padrão
    container.style.backgroundColor = getColorForCard(card);
    container.style.borderRadius = '8px';
    container.style.padding = '16px';
    container.style.display = 'flex';
    container.style.flexDirection = 'column';
    
    // Informação básica
    container.innerHTML = `
        <div style="font-size: 18px; font-weight: bold; color: white;">${card.name}</div>
        <div style="font-size: 14px; color: white; margin-top: 8px;">${card.card_type}</div>
        <div style="margin-top: 8px; color: white;">
            <strong>Custo:</strong> ${card.cost || 'N/A'}
            ${card.power ? `<strong style="margin-left: 8px;">Poder:</strong> ${card.power}` : ''}
        </div>
        <div style="margin-top: 16px; color: white; flex: 1;">
            ${card.text || 'Sem efeito'}
        </div>
    `;
}