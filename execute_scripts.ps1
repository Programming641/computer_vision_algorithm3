$env:PYTHONPATH = './'

# directory example. "videos/street6/resized"

$directory = Read-Host -Prompt 'enter your image directory. directory that contains all image files. "videos/street6/resized" for example'
$clrgrp_type = Read-Host -Prompt 'enter color group type. this type chooses the resolution of your images. this is used by putpix_into_clrgrp.py script
choices are: min1, min2, min3, clrgrp1,clrgrp2 ... for example.'

py tools/_execute_scripts.py $directory $clrgrp_type
If($LASTEXITCODE -eq 1){
   echo "error occurred in tools/_execute_scripts.py"
   echo uuuuuuuuuuy | choice
   exit
}

# right now, directory name is something like this. videos/street6/resized or videos/street6/resized/ and does not contain clrgrp_type. so add it
$dir_last_char = $directory.Substring($directory.Length - 1)
if( $dir_last_char -ne "/" ) {
   # last character is not /.
   $directory = $directory + "/" + $clrgrp_type
} else {
   $directory = $directory + $clrgrp_type
}

py algorithms/scnd_stage/execute_scripts.py $directory
If($LASTEXITCODE -eq 1){
   echo "error occurred in algorithms/scnd_stage/execute_scripts.py"
   echo uuuuuuuuuuy | choice
   exit
}

py algorithms/trd_stage/execute_scripts.py $directory
If($LASTEXITCODE -eq 1){
   echo "error occurred in algorithms/trd_stage/execute_scripts.py"
   echo uuuuuuuuuuy | choice
   exit
}


# beep to alert that all processing has ended
echo uuuuuuuuuuy | choice















