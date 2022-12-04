// <kor> From: https://doc.rust-lang.org/rust-by-example/std_misc/file/read_lines.html

//File::open expects a generic, AsRef<Path>. That's what read_lines() expects as input.

use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn get_elf_cals(
fn main() {
    let mut inv = Vec::new();

    if let Ok(lines) = read_lines("./test-data.txt") {
        // Consumes the iterator, returns an (Optional) String
        for line in lines {
            if let Ok(cals) = line {
		if 
                inv.push(cals);
            }
	    else {
		println!("a different kind of panic")
	    }
        }
    } else {
        println!("panic, idk, something");
    }

    for c in inv {
        println!("{}", c);
    }
}

// The output is wrapped in a Result to allow matching on errors
// Returns an Iterator to the Reader of the lines of the file.
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
