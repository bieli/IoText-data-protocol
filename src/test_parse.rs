use std::*;


// COPY -> PASTE to https://play.rust-lang.org/ for check parser prototype



//use std::intrinsics::type_name::*;
//use std::num::ParseIntError;
//use rust_decimal::Decimal;


struct MetricDataTypes {}

impl MetricDataTypes {
    const INTEGER: &str = "i";
    //const BOOL: &str = "b";
    //const DECIMAL: &str = "d";
    //const TEXT: &str = "t";
}


struct ItemType {}
impl ItemType {
    const TIME_UNIX_MILIS: &str = "t";
    const DEVICE_ID: &str = "d";
    //const METRIC: &str = "m";
}

#[derive(Debug)]
enum MetricValueType {
    IntegerItemType(i64),
    //BoolItemType(bool),
    //DecimalItemType(i64),
    //TextItemType(String),
}

#[derive(Debug)]
enum ItemTypeEnum {
    TimeUnixMilis(u64),
    DeviceId(String),
}

//#![feature(core_intrinsics)]
//fn print_type_of<T>(_: &T) {
//    println!("{}", unsafe { std::intrinsics::type_name::<T>() });
//}

fn main() {
    let item_parts: Vec<&str> = "t|3900237526042,d|device_name_001,m|val_water_level1=i:42"
        .split(',')
        .collect();

    for part in item_parts {
        println!("part: {}", part);
        let item_part: Vec<&str> = part.split('|').collect();
        println!("item_part: {:?}", item_part);
        let item_type_tmp: &str = item_part[0];
        let item_type_metric: &str = "m";
        if item_type_tmp.eq(item_type_metric) {
            println!("\tmetric: {}", item_part[1]);
            let metric_parts: Vec<&str> = item_part[1].split('=').collect();
            println!("\tmetric_parts: {:?}", metric_parts);
            //let metric_name: String = item_parts[0].to_string();
            //println!("metric_name: {}", metric_name);
            let metric_parts_values: Vec<&str> = metric_parts[1].split(':').collect();
            println!("\t\tmetric_parts_values: {:?}", metric_parts_values);
            match metric_parts_values[0] {
                MetricDataTypes::INTEGER => {
                    //value: Result<i64, _> = metric_parts_values[0].parse();
                    //let value: Option<i64> = metric_parts_values[0].parse();
                    //let value: Result<i64, ParseIntError> = metric_parts_values[0].parse::<i64>();
                    let value = match metric_parts_values[1].parse::<i64>() {
                        Ok(number) => number,
                        Err(_) => todo!(),
                    };
                    println!(
                        "\t\t\tIntegerItemType: {:?}",
                        MetricValueType::IntegerItemType(value)
                    )
                    //MetricValueType::IntegerItemType(value);
                }
                _ => println!("\t\t\tother"),
            }
        } else {
            match item_part[0] {
                ItemType::TIME_UNIX_MILIS => {
                    let value = match item_part[1].parse::<u64>() {
                        Ok(number) => number,
                        Err(_) => todo!(),
                    };
                    println!(
                        "\t\t\tTIME_UNIX_MILIS: {:?}",
                        ItemTypeEnum::TimeUnixMilis(value)
                    )
                }
                ItemType::DEVICE_ID => {
                
                    println!("\t\t\tDEVICE_ID: {:?}", ItemTypeEnum::DeviceId(String::from(item_part[1])))
                }
                val => {
                    println!("\t\t\t OTHER: {:?}", val);
                    //print_type_of(val)
                }
            }
            println!("\t\tcontext: {}", item_part[1])
        }
        /*match item_part.split('=').collect() {
            [item, details] => {
                println!("{:?}", item);
                println!("{:?}", details);
            }
            _ => println!("rest"),
        }*/
    }
    //assert_eq!(v, ["Mary", "had", "a", "little", "lamb"]);
    //println!("{:?}", v);
    //MetricValueType::IntegerItemType(0)
}

/*
STDOUT:


part: t|3900237526042
item_part: ["t", "3900237526042"]
			TIME_UNIX_MILIS: TimeUnixMilis(3900237526042)
		context: 3900237526042
part: d|device_name_001
item_part: ["d", "device_name_001"]
			DEVICE_ID: DeviceId("device_name_001")
		context: device_name_001
part: m|val_water_level1=i:42
item_part: ["m", "val_water_level1=i:42"]
	metric: val_water_level1=i:42
	metric_parts: ["val_water_level1", "i:42"]
		metric_parts_values: ["i", "42"]
			IntegerItemType: IntegerItemType(42)

*/
