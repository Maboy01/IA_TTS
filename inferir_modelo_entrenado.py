from __future__ import annotations

import argparse
import glob
import json
import os
from pathlib import Path

import torch
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer


DEFAULT_TEXT = "Hello, this is a voice trained with artificial intelligence."
DEFAULT_VOCODER = "vocoder_models/en/ljspeech/hifigan_v2"


def find_latest_run(checkpoints_dir: Path) -> Path:
    run_folders = glob.glob(str(checkpoints_dir / "tacotron_taller_3*"))
    if not run_folders:
        raise RuntimeError("No se encontro ninguna carpeta de entrenamiento en checkpoints.")
    return Path(max(run_folders, key=os.path.getctime))


def find_model_path(run_dir: Path) -> Path:
    best_model = run_dir / "best_model.pth"
    if best_model.exists():
        return best_model

    best_candidates = list(run_dir.glob("best_model*.pth"))
    if best_candidates:
        return max(best_candidates, key=lambda path: path.stat().st_ctime)

    checkpoints = list(run_dir.glob("checkpoint_*.pth"))
    if checkpoints:
        return max(checkpoints, key=lambda path: path.stat().st_ctime)

    raise RuntimeError("No se encontro ningun archivo de modelo utilizable.")


def maybe_load_vocoder(vocoder_name: str | None) -> tuple[str | None, str | None]:
    if not vocoder_name:
        return None, None

    manager = ModelManager(progress_bar=True, verbose=True)
    vocoder_path, vocoder_config_path, _ = manager.download_model(vocoder_name)
    return vocoder_path, vocoder_config_path


def can_use_mel_vocoder(config_path: Path) -> tuple[bool, str]:
    with config_path.open("r", encoding="utf-8") as file:
        config = json.load(file)

    out_channels = config.get("out_channels")
    if out_channels != 80:
        return (
            False,
            f"Este modelo genera {out_channels} canales. El vocoder HiFiGAN de LJSpeech espera 80 mel bins.",
        )
    return True, ""


def main() -> None:
    parser = argparse.ArgumentParser(description="Inferencia para el modelo TTS entrenado localmente.")
    parser.add_argument("--text", default=DEFAULT_TEXT, help="Texto a sintetizar.")
    parser.add_argument(
        "--checkpoints-dir",
        default="checkpoints",
        help="Carpeta donde estan las corridas de entrenamiento.",
    )
    parser.add_argument(
        "--output",
        default="resultado_taller.wav",
        help="Ruta del wav de salida.",
    )
    parser.add_argument(
        "--vocoder-name",
        default=DEFAULT_VOCODER,
        help="Nombre del vocoder publicado por Coqui. Usa cadena vacia para desactivarlo.",
    )
    parser.add_argument(
        "--no-vocoder",
        action="store_true",
        help="Desactiva el vocoder preentrenado y usa Griffin-Lim.",
    )
    args = parser.parse_args()

    root = Path.cwd()
    checkpoints_dir = (root / args.checkpoints_dir).resolve()
    output_path = (root / args.output).resolve()

    latest_run = find_latest_run(checkpoints_dir)
    model_path = find_model_path(latest_run)
    config_path = latest_run / "config.json"
    use_cuda = torch.cuda.is_available()
    vocoder_compatible, vocoder_reason = can_use_mel_vocoder(config_path)

    vocoder_path = None
    vocoder_config_path = None
    if not args.no_vocoder and args.vocoder_name and vocoder_compatible:
        try:
            vocoder_path, vocoder_config_path = maybe_load_vocoder(args.vocoder_name)
            print(f"Vocoder cargado: {args.vocoder_name}")
        except Exception as error:
            print(f"No se pudo cargar el vocoder. Se usara Griffin-Lim. Error: {error}")
    elif not vocoder_compatible:
        print(f"No se usara vocoder. {vocoder_reason}")

    print(f"Modelo: {model_path}")
    print(f"Config: {config_path}")
    print(f"CUDA: {use_cuda}")

    synthesizer = Synthesizer(
        tts_checkpoint=str(model_path),
        tts_config_path=str(config_path),
        vocoder_checkpoint=vocoder_path,
        vocoder_config=vocoder_config_path,
        use_cuda=use_cuda,
    )

    wav = synthesizer.tts(args.text)
    synthesizer.save_wav(wav, str(output_path))
    print(f"Audio generado: {output_path}")


if __name__ == "__main__":
    main()
