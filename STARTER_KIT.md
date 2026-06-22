# 🧑‍🎨 Primeros pasos con usuarios-mcp

Copiá y pegá lo que corresponda según tu app.

---

## 📋 MENSAJE PARA EL EQUIPO

Copiá el bloque de abajo y envialo por Slack/WhatsApp a tu equipo:

---

> 👋 **Equipo, ya tenemos usuarios sintéticos con IA.**
>
> Solo necesitan hacer esto UNA VEZ (5 minutos) y después solo chatean.
>
> ### Si usás Claude Desktop
>
> 1. Abrí la terminal de tu Mac (Cmd+Espacio, escribí "Terminal")
> 2. Copiá y pegá esto, apretá Enter:
> ```
> curl -LsSf https://astral.sh/uv/install.sh | sh
> ```
> 3. Abrí Claude Desktop. Andá a **Settings → MCP Servers → Add MCP Server**
> 4. En **Command** poné: `uvx`
> 5. En **Args** poné tres líneas:
>    - `--from`
>    - `git+https://github.com/Sebtiago/usuarios-mcp`
>    - `usuarios-mcp`
> 6. Cerrá y volvé a abrir Claude Desktop
> 7. Escribile esto a Claude:
>
> ```
> Inicializá usuarios en mi proyecto actual. Te voy a pasar archivos de
> investigación (entrevistas, notas) y quiero que me crees perfiles
> sintéticos de usuarios para validar diseños.
> ```
>
> Listo. De ahora en más solo chateás:
> - "Creá usuarios sintéticos de estas entrevistas"
> - "Validá este diseño contra María"
> - "¿Cómo va el proyecto?"
>
> ### Si usás Codex Desktop
>
> 1. Abrí la terminal de tu Mac (Cmd+Espacio, escribí "Terminal")
> 2. Copiá y pegá esto, apretá Enter:
> ```
> curl -LsSf https://astral.sh/uv/install.sh | sh
> ```
> 3. Abrí Codex Desktop. Andá a **Settings → MCP**
> 4. Agregá un nuevo server con:
>    - **Command**: `uvx`
>    - **Args** (tres líneas):
>      - `--from`
>      - `git+https://github.com/Sebtiago/usuarios-mcp`
>      - `usuarios-mcp`
> 5. Reiniciá Codex
> 6. Escribile:
> ```
> Inicializá usuarios en mi proyecto actual y prepará todo para analizar
> investigación de diseño de servicios.
> ```
>
> ---
> Cualquier cosa me avisan. Una vez configurado no hay que tocar nada más.

---

## 🎯 Los 4 mensajes que van a usar siempre

Después de la configuración inicial, estos son los únicos mensajes que necesitan:

| Quieren hacer | Le dicen a la IA |
|---|---|
| **Crear perfiles** | *"Analizame las entrevistas de la carpeta research y creame usuarios sintéticos"* |
| **Validar un diseño** | *"Validá esta propuesta de onboarding contra el perfil de María"* |
| **Ver el estado** | *"¿Cómo va el proyecto de usuarios?"* |
| **Refinar un perfil** | *"Actualizá el perfil de Juan con estos nuevos hallazgos..."* |

---

## 🆘 Si algo falla

Decile a la IA: *"¿Podés ejecutar quick_status y decirme cómo está el proyecto?"*

Eso le da a la IA un dashboard completo y sabe exactamente qué falta.

---

## 📦 Repo

github.com/Sebtiago/usuarios-mcp
