echo "execute matches_for_shapes_that_separate.py"
py algorithms/scnd_stage/changes_btwn_frames/matches_for_shapes_that_separate.py $Args[0]
# result data file path -> 1.data

echo "execute find_fusing_shapes.py"
py algorithms/scnd_stage/changes_btwn_frames/find_fusing_shapes.py $Args[0]
# result data file path -> 2.data

echo "execute matches_for_pixch_on_notfnd_shapes.py"
py algorithms/scnd_stage/changes_btwn_frames/matches_for_pixch_on_notfnd_shapes.py $Args[0]
# result data file path -> 4.data



# beep to alert that all processing has ended
echo uuuuuuuuuuy | choice

















