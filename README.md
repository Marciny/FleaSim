##### FleaSim
######Game/simulation of fleas' life

######Aim : eat and breed and maybe not die.
With each bite fleas get bigger and have more biting power.   
Each bite create blood mark, high concentration of blood marks invokes deadly slaps (pictured as big circles).   
Overall high number of blood marks invokes also deadly scratches. Certain area may be bitten several times (default: 2), which is represented by transparent red color (full red - maximal degree).  
Biting also increases potency attribute needed for procreation, which has to be replenished.   
Fleas are of different sex - male (black) and female (purple).   
Baby fleas spawn at random location instantly after close encounters of different sex fleas.   
Game ends when all fleas die.  
There are three types of powerups appearing once in a while -  2x jump power, 2x bite power, and new flea spawn.

######Descriptions on screen (visible by toggling with 't' key):
On the top left there is jump power bar, next to it lies potency bar.  
Fleaseconds - sum of population size * each passed second  
Bitten area - percentage of actual bitten area to the maximal possible level of carnage.

######Controls :
* LMB(hold) - jump with speed depending on holding time in the direction of mouse cursor
* RMB - bite / procreate if in close proximity to flea of another sex
* SPACE - center camera on player's flea
* TAB - toggle display of score and other parameters
* ESCAPE - quit

###### Made with:
* python 3.4
* pygame 1.9.2a0
* numpy
