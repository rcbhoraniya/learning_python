export class Production {
    constructor(plant, date, shift, operator_name, no_of_winderman, product_code, end_reading, start_reading, wastage, ) {

        this.plant = plant;
        this.date = date;
        this.shift = shift;
        this.operator_name = operator_name;
        this.no_of_winderman = no_of_winderman;
        this.product_code = product_code;
        this.end_reading = end_reading;
        this.start_reading = start_reading;
        this.wastage = wastage;
    }
}

export class User {
    constructor(username, email, password, first_name, last_name) {
        this.username = username;
        this.email = email;
        this.password = password;
        this.first_name = first_name;
        this.last_name = last_name;
    }
}

export class Product {
    constructor(id, product_code, color_marking_on_bobin, tape_color, denier, gramage, tape_width, cutter_spacing, stock_of_bobin, streanth_per_tape_in_kg, elongation_percent, tenacity, pp_percent, filler_percent, shiner_percent, color_percent, tpt_percent, uv_percent, color_name) {
        this.id = id;
        this.product_code = product_code;
        this.color_marking_on_bobin = color_marking_on_bobin;
        this.tape_color = tape_color;
        this.denier = denier;
        this.gramage = gramage;
        this.tape_width = tape_width;
        this.cutter_spacing = cutter_spacing;
        this.stock_of_bobin = stock_of_bobin;
        this.streanth_per_tape_in_kg = streanth_per_tape_in_kg;
        this.elongation_percent = elongation_percent;
        this.tenacity = tenacity;
        this.pp_percent = pp_percent;
        this.filler_percent = filler_percent;
        this.shiner_percent = shiner_percent;
        this.color_percent = color_percent;
        this.tpt_percent = tpt_percent;
        this.uv_percent = uv_percent;
        this.color_name = color_name;

    }
}