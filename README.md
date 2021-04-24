# NieR-Audio-Tools
Tools for working with audio in NieR Replicant and NieR Automata.

## Requirements
Requires Python: https://www.python.org/downloads

For playing and converting .wem files, you can use **[Foobar 2000](https://www.foobar2000.org/download)** with the **[vgmstream](https://www.foobar2000.org/components/view/foo_input_vgmstream)** plugin.

Alternatively, you can convert .wem files to .ogg using **[ww2ogg](https://github.com/hcs64/ww2ogg)**.

If you want to create new .wem files, you need to use **[Wwise](https://www.audiokinetic.com/products/wwise/)**. If you are having trouble launching WWise, try using WWise 2016 32 bit.

Be aware that .wem files created with Wwise may not always work in game due to required data being missing from the .wem file.

## Tools
### replicant_PCK_Util.py
For extracting and repacking NieR Replicant **.pck** files.

Usage: `nier_PCK_Util.py <PCK Path> <OPTIONS>`

You can also drag a .pck file onto the program to extract it.
* `-e <Extract Directory>` Extract WEMs or BNKs from the PCK to the directory provided. (Optional)
* `-r <Repack Directory>` Repack the PCK with WEMs or BNKs at the directory provided. (Optional)
* `-x <Export Directory>` Export the repacked PCK to the directory provided. The repack directory (-r) option must be used. (Optional)

Example Command: `replicant_PCK_Util.py stream2.pck -r stream2_extract\repack`

### nier_BNK_Util.py
For extracting, editing and repacking NieR Replicant and NieR Automata **.bnk** files.

(Coming soon)

### nier_WSP_Util.py
For extracting and repacking NieR Automata **.wsp** files.

Usage: `nier_WSP_Util.py <PCK Path> <OPTIONS>`

You can also drag a .wsp file onto the program to extract it.
* `-e <Extract Directory>` Extract WEMs from the WSP to the directory provided. (Optional)
* `-r <Repack Directory>` Repack the WSP with WEMs at the directory provided. (Optional)
* `-x <Export Directory>` Export the repacked WSP to the directory provided. The repack directory (-r) option must be used. (Optional)

**NOTE:** Repacking will not work unless the .wem file has additional data that the game requires.

If you are able to get a custom .wem file in a .wsp to work, let me know.

Example Command: `nier_WSP_Util.py BGM_0_005.wsp -e testdirectory`