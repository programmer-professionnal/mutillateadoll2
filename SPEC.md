# Mutilate a Doll 2 - Enhanced Clone
## Especificación Técnica del Proyecto

---

## 1. Overview

**Nombre del Proyecto:** Mutillateadoll2
**Tipo:** Sandbox de física / juego de destrucción
**Descripción:** Un sandbox de física avanzadas sobre mutilar muñecos ragdoll con más de 200+ herramientas, armas, y poderes. Inspirado en Mutilate-a-Doll 2 pero con innovaciones propias.
**Target:** Windows executable (.exe)

---

## 2. Características Core

### 2.1 Sistema de Ragdolls
- **Ragdoll humanoide completo:** Cabeza, torso, brazos (superior/inferior), piernas (superior/inferior), manos, pies
- **Joint system:** Simulación de vértebras para movimiento realista
- **Spawning:** Múltiples ragdolls simultáneos (límite configurable)
- **Customización:** Color de piel, tamaño, género (opcional)
- **Estados:** Intacto, herido, destruido, regenerado

### 2.2 Sistema de Herramientas (200+ items)

#### Armas Cuerpo a Cuerpo
- Cuchillos, espadas, machetes, hachas
- Batas, cadenas, martillos, llaves inglesas
- Sierras eléctricas,金刚石, lanzas

#### Armas de Fuego
- Pistolas, revólveres, rifles, escopetas
- Ametralladoras,狙击步枪, lanzacohetes
- Armas especiales: láser, plasma, electromagnéticas

#### Explosivos
- Dinamita, C4, granadas
- Bombas nucleares (mini), minas terrestres
- Cargadores remotamente detonables

#### Herramientas de Construcción
- Bloques de construcción (madera, metal, concreto)
- Placas de presión, botones, temporizadores
- Motores, poleas, resortes, bisagras
- Sistemas de agua/fluido

### 2.3 Sistema de Poderes (Powers)
- **Fuego:** Quemar objetos/ragdolls
- **Hielo:** Congelar目标和创建冰墙
- **Electricidad:** Electrocutar y activar motores
- **Gravedad:** Manipular gravedad mundial
- **Viento:** Crear corrientes de aire
- **Transmutar:** Convertir objetos (oro, pizza, cookies)
- **Explosión:** Olas de choque
- **Rayos X:** Ver estructura interna
- **Silenciar:** Quitar sonido
- **Regenerar:** Restaurar ragdolls
- **Mutar:** Transformar ragdolls en monstruos
- **Crear:** Generar nuevos ragdolls desde menú

### 2.4Sistema de Partículas y Efectos
- **Sangre:** Partículas rougesque salen al dañar ragdolls
- **Fuego:** Partículas ardientes con comportamiento realista
- **Humo:** Efecto de humo con disipación gradual
- **Polvo:** Partículas de debris al impactar
- **Chispas:** Al cortar objetos metálicos
- **Electricidad:** Arco de voltaje entre puntos

### 2.5 Sistema de Edición
- **Editor de nivel:** Crear escenarios personalizados
- **Colocación libre:** Arrastrar y posicionar objetos
- **Rotación:** Girar objetos en 2D (360°)
- **Escala:** Cambiar tamaño de objetos
- **Agrupación:** Crear estructuras complejas
- **Capas:** Organización por z-index
- **Snap to grid:** Alineación precisa

### 2.6 Sistema de Guardado
- **Slots de guardado:** 10+ perfiles
- **Capturas de pantalla:** Guardar estado visual
- **Exportar/Importar:** Compartir niveles
- **Custom items:** Guardar objetos personalizados

### 2.7 UI Sistema
- **Toolbox lateral:** Acceso rápido a herramientas
- **Menú principal:** Nuevo, Cargar, Guardar, Opciones
- **Barra de herramientas:** Herramientas seleccionada actualmente
- **Panel de propiedades:** Modificar objeto seleccionado
- **Minimapa:** Vista general del escenario
- **Configuraciones:** Gráficos, audio, sangre ON/OFF

---

## 3. Innovaciones Propias

### 3.1 Modo Historia (Opcional)
- Niveles con objetivos específicos
- Puzzles de física
- Desafíos cronometrados

### 3.2 Ragdoll AI
- Ragdolls que reaccionan al daño
- Intentos de escapar/defenderse
- Comportamiento adaptativo

### 3.3 Sistema de Logros
- Logros por destrucción/construcción
- Tabla de clasificación

### 3.4 Multiplayer Local
- Competencia local de destrucción
- Modos: puntuación, tiempo

### 3.5 Herramientas de Redeem
- Código para desbloquear items secretos

---

## 4. Arquitectura Técnica

### 4.1 Dependencias
```
Python 3.10+
Pygame 2.x - Renderizado y input
Pymunk 6.x - Física 2D
NumPy - Cálculos matemáticos
PyInstaller - Compilación a .exe
```

### 4.2 Estructura de Archivos
```
/mutillateadoll2
├── main.py              # Entry point
├── core/
│   ├── physics.py      # Pymunk wrapper
│   ├── ragdoll.py      # Ragdoll system
│   ├── tools.py        # Tool definitions
│   ├── powers.py       # Power effects
│   └── effects.py      # Particle system
├── ui/
│   ├── menu.py         # Main menu
│   ├── toolbox.py     # Tool selection
│   └── hud.py          # In-game UI
├── data/
│   ├── items.json     # Tool definitions
│   ├── powers.json   # Power definitions
│   └── sounds/        # Audio files
└── build/             # Compiled output
```

### 4.3 Rendimiento
- Target: 60 FPS estable
- Capacidad: 50+ ragdolls simultáneos
- Optimización: Spatial hashing para colisiones

---

## 5. Controles

| Acción | Tecla |
|--------|-------|
| Seleccionar herramienta | Clic izquierdo |
| Colocar/Mover objeto | Arrastrar |
| Eliminar objeto | Delete/Supr |
| Rotar objeto | R (mientras se sujeta) |
| Escalar objeto | Scroll del mouse |
| Menú pausa | Escape |
| Nuevo ragdoll | N |
| Reiniciar nivel | F5 |

---

## 6.consideraciones adicionales

- **Seguridad:** Sin contenido realista o gore excesivo
- **Rendimiento:** Código optimizado para Python puro
- **Modding:** Potencial para addons futuros
- **Expresiones artísticas permitidas:** Estilo cartoon