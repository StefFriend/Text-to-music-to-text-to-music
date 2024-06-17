## LP-Music Caps installation

```bash

pip install -r requirements.txt

wget https://huggingface.co/seungheondoh/lp-music-caps/resolve/main/transfer.pth -O exp/transfer/lp_music_caps/last.pth
```
(Please install torch according to your [CUDA version](https://pytorch.org/get-started/previous-versions/).)

Leave here captioning2.py since it is needed for infinitystem.
