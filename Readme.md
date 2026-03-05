            ┌─────────────┐
            │ Supervisor  │
            └──────┬──────┘
                   │
   ┌───────────────┼────────────────┐
   ↓               ↓                ↓
Greeting     Preferences        Guardrail
   ↓               ↓
   └──────→ Recipe Agent
               ↓
           Step Mode
               ↓
           Feedback



User: hello
supervisor → greeting
greeting → supervisor
supervisor → collect_preferences
collect_preferences → supervisor
supervisor → generate_recipe
generate_recipe → supervisor
supervisor → step_mode
step_mode → supervisor
supervisor → collect_feedback
collect_feedback → END