echo "execute cross_check_all_low_level_algo_acrs_all_files.py"
py algorithms/scnd_stage/cross_check_all_low_level_algo_acrs_all_files.py $Args[0]

echo "execute find_shapes_match_types.py"
py algorithms/scnd_stage/find_shapes_match_types.py $Args[0]
# output filepath -> shp_match_types/data/matched_pixels.data and not_classified.data

echo "execute match_neighbor_by_relpos_shp_nbr.py"
py algorithms/scnd_stage/match_neighbor_by_relpos_shp_nbr.py $Args[0]
# output filename -> verified2.data

echo "execute find_shapes_from_Nfnd_shapes_by_relpos.py"
py algorithms/scnd_stage/find_shapes_from_Nfnd_shapes_by_relpos.py $Args[0]
# output filepath -> relpos_nbr/data/1.data

echo "execute find_consecutively_missing_shapes2.py"
py algorithms/scnd_stage/find_consecutively_missing_shapes2.py $Args[0]
# output filepath -> consecutive_missed/data/2.data

echo "execute find_consecutively_missing_shapes3.py"
py algorithms/scnd_stage/find_consecutively_missing_shapes3.py $Args[0]
# output filepath -> consecutive_missed/data/3.data

echo "execute find_consecutively_missing_shapes4.py"
py algorithms/scnd_stage/find_consecutively_missing_shapes4.py $Args[0]
# output filepath -> consecutive_missed/data/possible_matches.data

echo "execute find_nbr_matches_from_Nfnd_shapes.py"
py algorithms/scnd_stage/find_nbr_matches_from_Nfnd_shapes.py $Args[0]
# output filepath -> nbr_matches.data

echo "execute find_consecutively_missing_shapes5.py"
py algorithms/scnd_stage/find_consecutively_missing_shapes5.py $Args[0]
# output filepath -> consecutive_missed/data/5.data

echo "execute find_shapes_from_Nfnd_shapes.py"
py algorithms/scnd_stage/find_shapes_from_Nfnd_shapes.py $Args[0]
# output filename -> verified5.data


echo "execute find_shapes_from_Nfnd_shapes_by_relpos2.py"
py algorithms/scnd_stage/find_shapes_from_Nfnd_shapes_by_relpos2.py $Args[0]
# output filepath -> relpos_nbr/data/2.data

echo "execute find_shapes_from_Nfnd_shapes_by_relpos3.py"
py algorithms/scnd_stage/find_shapes_from_Nfnd_shapes_by_relpos3.py $Args[0]
# output filepath -> relpos_nbr/data/3.data


echo "execute verify_shapes_from_Nfnd_shapes_by_relpos3.py"
py algorithms/scnd_stage/verify_shapes_from_Nfnd_shapes_by_relpos3.py $Args[0]
# output filepath -> relpos_nbr/data/verified3.data

echo "execute find_moving_together_shapes.py"
py algorithms/scnd_stage/find_moving_together_shapes.py $Args[0]
# output filepath -> move_together/data/move_together.data

echo "execute correct_wrong_matches.py"
py algorithms/scnd_stage/correct_wrong_matches.py $Args[0]
# output filepath -> correct_matches/data/1.data


# beep to alert that all processing has ended
echo uuuuuuuuuuy | choice

















