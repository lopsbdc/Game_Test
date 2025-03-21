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
    
    // Verificar se o template tem zonas definidas
    if (template && Object.keys(template.zones || {}).length === 0) {
        // Template sem zonas, usar visualização padrão
        renderDefaultCard(card, container, config);
        return;
    }
    
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
/**
 * Renderiza uma zona específica do template
 */
function renderZone(id, zone, card, container, config) {
    // Criar elemento para a zona
    const zoneElement = document.createElement('div');
    zoneElement.className = 'template-zone';
    zoneElement.dataset.zoneId = id;
    
    // Posicionar e dimensionar a zona
    zoneElement.style.position = 'absolute';
    zoneElement.style.left = `${zone.x * config.scale}px`;
    zoneElement.style.top = `${zone.y * config.scale}px`;
    zoneElement.style.width = `${zone.width * config.scale}px`;
    zoneElement.style.height = `${zone.height * config.scale}px`;
    zoneElement.style.zIndex = (zone.z_index || 1) + 1; // +1 para ficar acima do overlay
    
    // Aplicar estilos específicos (se definidos no template)
    if (zone.opacity !== undefined) {
        zoneElement.style.opacity = zone.opacity;
    }
    
    if (zone.background_color) {
        zoneElement.style.backgroundColor = zone.background_color;
    }
    
    if (zone.border_color && zone.border_width) {
        zoneElement.style.borderColor = zone.border_color;
        zoneElement.style.borderWidth = `${zone.border_width}px`;
        zoneElement.style.borderStyle = 'solid';
    }
    
    if (zone.type === 'circle' || zone.border_radius) {
        // Para círculos o raio é 50%
        if (zone.type === 'circle') {
            zoneElement.style.borderRadius = '50%';
        } else if (zone.border_radius) {
            zoneElement.style.borderRadius = `${zone.border_radius * config.scale}px`;
        }
    }
    
    // Renderizar conteúdo baseado no tipo de zona
    switch (zone.type) {
        case 'text':
            renderTextZone(zone, card, zoneElement, config);
            break;
            
        case 'image':
            renderImageZone(zone, card, zoneElement, config);
            break;
            
        case 'icon':
            renderIconZone(zone, card, zoneElement, config);
            break;
            
        default:
            // Para outros tipos, mostrar apenas o ID da zona
            zoneElement.textContent = id;
    }
    
    // Adicionar zona ao container
    container.appendChild(zoneElement);
    
    // Adicionar eventos interativos se necessário
    if (config.interactive && config.mode === 'edit') {
        makeZoneInteractive(zoneElement, id, zone);
    }
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

/**
 * Renderiza uma zona de texto
 */
function renderTextZone(zone, card, element, config) {
    // Campo a ser mostrado
    const fieldName = zone.field_name || 'name';
    
    // Obter o valor do campo da carta
    let content = card[fieldName] || '';
    
    // Configuração de texto
    element.style.fontFamily = zone.font_family || 'Arial, sans-serif';
    element.style.fontSize = `${(zone.font_size || 12) * config.scale}px`;
    element.style.textAlign = zone.text_align || 'left';
    element.style.color = zone.text_color || '#FFFFFF';
    
    // Alinhamento vertical (centralizado por padrão)
    element.style.display = 'flex';
    element.style.alignItems = 'center';
    
    // Alinhamento horizontal baseado no text-align
    switch (zone.text_align) {
        case 'center':
            element.style.justifyContent = 'center';
            break;
        case 'right':
            element.style.justifyContent = 'flex-end';
            break;
        default:
            element.style.justifyContent = 'flex-start';
    }
    
    // Definir conteúdo
    element.textContent = content;
}

/**
 * Renderiza uma zona de imagem
 */
function renderImageZone(zone, card, element, config) {
    // Configurar estilo do container
    element.style.overflow = 'hidden';
    element.style.display = 'flex';
    element.style.alignItems = 'center';
    element.style.justifyContent = 'center';
    
    // Verificar se a carta tem imagem
    if (card.image_url) {
        const img = document.createElement('img');
        img.src = card.image_url;
        img.alt = card.name;
        
        // Aplicar ajustes de imagem
        img.style.width = '100%';
        img.style.height = '100%';
        img.style.objectFit = zone.image_fit || 'contain';
        img.style.objectPosition = zone.image_position || 'center';
        
        element.appendChild(img);
    } else {
        // Placeholder para quando não há imagem
        element.style.backgroundColor = 'rgba(0, 0, 0, 0.2)';
        element.style.border = '1px dashed rgba(255, 255, 255, 0.3)';
        
        const placeholder = document.createElement('div');
        placeholder.textContent = 'Sem imagem';
        placeholder.style.color = 'rgba(255, 255, 255, 0.5)';
        placeholder.style.fontSize = `${8 * config.scale}px`;
        element.appendChild(placeholder);
    }
}

/**
 * Renderiza uma zona de ícone
 */
function renderIconZone(zone, card, element, config) {
    // Ícones baseados em características da carta
    let iconName = zone.icon_name || '⚡';
    
    // Configurar estilo
    element.style.display = 'flex';
    element.style.alignItems = 'center';
    element.style.justifyContent = 'center';
    element.style.fontSize = `${(zone.font_size || 24) * config.scale}px`;
    
    // Adicionar o ícone
    element.textContent = iconName;
}

/**
 * Aplica interatividade a uma zona (para modo de edição)
 */
function makeZoneInteractive(zoneElement, id, zone) {
    // Adicionar classe visual para indicar que é interativo
    zoneElement.classList.add('interactive-zone');
    
    // Adicionar controles de edição
    const controlsWrapper = document.createElement('div');
    controlsWrapper.className = 'zone-controls';
    controlsWrapper.style.position = 'absolute';
    controlsWrapper.style.top = '-20px';
    controlsWrapper.style.right = '0';
    controlsWrapper.style.zIndex = '100';
    controlsWrapper.style.display = 'none';
    
    // Botão para mover
    const moveBtn = document.createElement('button');
    moveBtn.className = 'move-btn';
    moveBtn.innerHTML = '🔄';
    moveBtn.title = 'Mover';
    moveBtn.style.width = '24px';
    moveBtn.style.height = '24px';
    moveBtn.style.marginRight = '5px';
    moveBtn.style.background = '#4f46e5';
    moveBtn.style.border = 'none';
    moveBtn.style.borderRadius = '4px';
    moveBtn.style.color = 'white';
    moveBtn.style.cursor = 'move';
    
    // Botão para redimensionar
    const resizeBtn = document.createElement('button');
    resizeBtn.className = 'resize-btn';
    resizeBtn.innerHTML = '⤡';
    resizeBtn.title = 'Redimensionar';
    resizeBtn.style.width = '24px';
    resizeBtn.style.height = '24px';
    resizeBtn.style.background = '#2563eb';
    resizeBtn.style.border = 'none';
    resizeBtn.style.borderRadius = '4px';
    resizeBtn.style.color = 'white';
    resizeBtn.style.cursor = 'se-resize';
    
    controlsWrapper.appendChild(moveBtn);
    controlsWrapper.appendChild(resizeBtn);
    zoneElement.appendChild(controlsWrapper);
    
    // Mostrar controles ao passar o mouse
    zoneElement.addEventListener('mouseenter', () => {
        controlsWrapper.style.display = 'flex';
        zoneElement.style.boxShadow = '0 0 0 2px rgba(79, 70, 229, 0.6)';
    });
    
    zoneElement.addEventListener('mouseleave', () => {
        controlsWrapper.style.display = 'none';
        zoneElement.style.boxShadow = 'none';
    });
    
    // Evento de clique para edição
    zoneElement.addEventListener('click', () => {
        // Disparar evento customizado com informações da zona
        const event = new CustomEvent('zone-selected', {
            detail: { id, zone }
        });
        zoneElement.dispatchEvent(event);
        
        // Propagar o evento para o documento
        document.dispatchEvent(event);
    });
}