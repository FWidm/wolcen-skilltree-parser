# Wolcen Skilltree Parser

- obtain data from the game files via [WolcenExtractor](https://github.com/gabriel-dehan/WolcenExtractor):
```bash
wolcen_extractor.exe extract --source "I:\SteamLibrary\steamapps\common\Wolcen" --dest "out" --only "lib,umbra,script" --trace
```
- add specific folders to the iput folder
    - add the localization folder here
    - add the Umbra folder here from your extracted Game files (`Game/Umbra`)
-  Graphics can be found in : `out\Game\Libs\UI\u_passiveskills`