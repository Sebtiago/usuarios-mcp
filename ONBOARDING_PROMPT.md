# 🪄 Copiá, pegá, listo

**Mandale esto a tu equipo. Es un solo mensaje.**
Lo pegan en Claude Desktop y la IA hace todo.

---

Necesito configurar mi compu para poder crear usuarios sintéticos
con una herramienta que se llama usuarios-mcp. Guiame paso a paso
como si nunca hubiera abierto una terminal. Hablame en español.

## Paso 1: Instalar uv
¿Podés ejecutar este comando por mí?
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Si no podés, decime exactamente qué teclear y dónde.

## Paso 2: Conectar usuarios-mcp
Necesito agregar un MCP server con estos datos:
- Command: `uvx`
- Args (uno por línea):
  `--from`
  `git+https://github.com/Sebtiago/usuarios-mcp`
  `usuarios-mcp`

Decime dónde hacer clic: menú → opción → botón → campo.

## Paso 3: Probar
Cuando reinicie Claude Desktop, voy a abrir un chat nuevo y decirte:
"Hola, ¿está funcionando usuarios-mcp?"
Quiero que me respondas usando la herramienta quick_status
para mostrarme que todo está listo. Si no la encontrás, avisame
y revisamos la configuración.

---

⚠️ Después de configurar, reiniciá Claude Desktop y abrí un chat nuevo.
Ahí ya vas a poder decir cosas como:
- "Creá usuarios sintéticos de mis entrevistas"
- "Validá este diseño contra el perfil de María"
- "¿Cómo va el proyecto?"

