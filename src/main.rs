fn fibonacci(n: u32) -> Vec<u64> {
    let mut seq = Vec::with_capacity(n as usize);
    for i in 0..n {
        let val = match i {
            0 => 0,
            1 => 1,
            _ => seq[(i - 1) as usize] + seq[(i - 2) as usize],
        };
        seq.push(val);
    }
    seq
}

fn main() {
    let n = 10;
    for number in fibonacci(n) {
        println!("{}", number);
    }
}
