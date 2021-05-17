# NieR-Audio-Tools
Tools for working with audio in NieR Replicant and NieR Automata.

## Requirements
Requires Python: https://www.python.org/downloads

For playing and converting .wem files, you can use **[Foobar 2000](https://www.foobar2000.org/download)** with the **[vgmstream](https://www.foobar2000.org/components/view/foo_input_vgmstream)** plugin.

Alternatively, you can convert .wem files to .ogg using **[ww2ogg](https://github.com/hcs64/ww2ogg)**.

If you want to create new .wem files, you need to use **[Wwise](https://www.audiokinetic.com/products/wwise/)**. If you are having trouble launching WWise, try using WWise 2016 32 bit.

**Be sure to back up files before you replace them.**
## Tools
### replicant_PCK_Util.py

*V3 - 5/17/2021*

For extracting and repacking NieR Replicant **.pck** files.

Usage: `replicant_PCK_Util.py <PCK Path> <OPTIONS>`

You can also drag a .pck file onto the program to extract it.

**Be sure that you have SoundNames_replicant.csv in the same directory as the program.**
* `-e <Extract Directory>` Extract WEMs or BNKs from the PCK to the directory provided. (Optional)
* `-r <Repack Directory>` Repack the PCK with WEMs or BNKs at the directory provided. (Optional)
* `-x <Export Directory>` Export the repacked PCK to the directory provided. The repack directory (-r) option must be used. (Optional)

Example Command: `replicant_PCK_Util.py stream2.pck -r stream2_extract\repack`

**V3 Changes:**
* Rewritten PCK structure to be faster and more accurate.
* BNKs now extract with names.
* Repacking is now done via ID instead of index.
* Removed index numbers from WEMs and moved WEM ID to end of file name.
* Performance improvements - stream.pck extract time from ~15 seconds to ~4.5 seconds.

**NOTE: If you are updating from V1 or V2, you cannot repack with WEMs extracted from those versions.**

**Run "update_OLD_WEMNames_replicant.py" on the repack directory to fix the old file names to be able to use them.**

### nier_BNK_Util.py

*V1 - 5/17/2021*

For extracting and repacking NieR Replicant and NieR Automata **.bnk** files.

Also should support other games that use Wwise .bnk files.

Usage: `nier_BNK_Util.py <BNK Path> <OPTIONS>`

You can also drag a .bnk file onto the program to extract it.

**Be sure that you have SoundNames_XXX.csv files in the same directory as the program.**
* `-e <Extract Directory>` Extract WEMs from the BNK to the directory provided. (Optional)
* `-r <Repack Directory>` Repack the BNK with WEMs at the directory provided. Reads all subdirectories. (Optional)
* `-x <Export Directory>` Export the repacked BNK to the directory provided. The repack directory (-r) option must be used. (Optional)

Example Command: `nier_BNK_Util.py "path\to\media_extract\english(us)\3-SE_media-4051147064.bnk" -r "path\to\media_extract\repack"`

HIRC and music loop point editing to be added in a future update.

### updateWEMNames_replicant/automata.py

Use this when SoundNames_XXX.csv is updated to update the names of WEM files in the provided directory.

### nier_WSP_Util.py

For extracting and repacking NieR Automata **.wsp** files.

Usage: `nier_WSP_Util.py <WSP Path> <OPTIONS>`

You can also drag a .wsp file onto the program to extract it.
* `-e <Extract Directory>` Extract WEMs from the WSP to the directory provided. (Optional)
* `-r <Repack Directory>` Repack the WSP with WEMs at the directory provided. (Optional)
* `-x <Export Directory>` Export the repacked WSP to the directory provided. The repack directory (-r) option must be used. (Optional)

**NOTE:** Repacking will not work unless the .wem file has additional data that the game requires.

If you are able to get a custom .wem file in a .wsp to work, let me know.

Example Command: `nier_WSP_Util.py BGM_0_005.wsp -e testdirectory`

## Credits

Thank you to:
* **[bnnm](https://github.com/bnnm)** - For wwiser tool and help with wwise event names.
* **[Silvris](https://github.com/Silvris)** - Help with random wwise questions
