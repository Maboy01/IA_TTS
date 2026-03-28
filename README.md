# IA_TTS
# REVISAR EL ARCHIVO `taller_fundamentos_deeplearning_local_windows.ipynb` AHI ESTA TODO EL CODIGO
Proyecto para entrenar e inferir un modelo de texto a voz en Windows usando Coqui TTS.

## Contenido

- `TTS/`: submodulo apuntando al repositorio oficial de Coqui TTS.
- `download_ljspeech_subset.ps1`: descarga y prepara un subconjunto del dataset LJSpeech.
- `taller_fundamentos_deeplearning_local_windows.ipynb`: notebook principal para entrenamiento local.
- `inferir_modelo_entrenado.py`: script de inferencia usando el ultimo checkpoint disponible.
- `README_LOCAL_WINDOWS.md`: guia corta de uso en Windows.

## Primeros pasos

```powershell
git clone https://github.com/Maboy01/IA_TTS.git
cd IA_TTS
git submodule update --init --recursive
```

Despues de inicializar el submodulo, sigue la guia en `README_LOCAL_WINDOWS.md`.
