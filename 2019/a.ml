open Core

let sum_file filename =
  let file = In_channel.create filename in
  let fuel_req s =
    let m = Float.of_string s in
    (Float.round_down (m /. 3.)) -. 2.
  in
  let numbers = List.map ~f:fuel_req (In_channel.input_lines file) in
  let sum = List.fold ~init:0 ~f:(+.) numbers in
  In_channel.close file;
  sum;;

sum_file "input.txt";;
