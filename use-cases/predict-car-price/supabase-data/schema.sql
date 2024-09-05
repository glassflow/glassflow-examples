CREATE TABLE car_price_data (
    id UUID PRIMARY KEY,
    model TEXT NOT NULL,
    year INT NOT NULL,
    price INT NOT NULL,
    transmission TEXT CHECK (transmission IN ('manual', 'automatic')) NOT NULL,
    mileage INT NOT NULL,
    fuelType TEXT CHECK (fuelType IN ('petrol', 'diesel', 'electric', 'hybrid')) NOT NULL,
    tax INT NOT NULL,
    mpg INT NOT NULL,
    engineSize DECIMAL(3,1) NOT NULL
);
