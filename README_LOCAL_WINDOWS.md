# Flujo local Windows

## Orden recomendado

1. Activa el entorno:

```powershell
cd C:\Users\USER\Documents\Yamin
.\.venv\Scripts\Activate.ps1
```

2. Descarga y prepara el dataset:

```powershell
.\download_ljspeech_subset.ps1
```

3. Abre el notebook local:

```powershell
jupyter notebook .\taller_fundamentos_deeplearning_local_windows.ipynb
```

## Que hace el notebook local

- Usa rutas de Windows y del proyecto actual
- Genera `config.local.json`
- Lanza el entrenamiento con `train_tts.py`
- Busca checkpoints en `.\checkpoints`
- Hace inferencia con `Synthesizer`

## Notas

- El dataset completo pesa bastante y puede tardar.
- El notebook original de Colab se conserva intacto.
- Esta version usa valores mas seguros para Windows: menos workers y batch mas pequeno.
