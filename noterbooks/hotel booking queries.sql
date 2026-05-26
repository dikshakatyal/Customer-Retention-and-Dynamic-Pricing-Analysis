
USE hotel_booking_project;


CREATE TABLE hotel_bookings (
    hotel VARCHAR(50),
    lead_time INT,
    arrival_date DATE,
    stays_weekend_nights INT,
    stays_week_nights INT,
    adults INT,
    children INT,
    meal VARCHAR(10),
    country VARCHAR(10),
    adr FLOAT,
    is_canceled INT
);

SHOW tables;
SELECT COUNT(*) AS total_bookings 
FROM hotel_booking_10000;

SELECT * FROM hotel_booking_10000 LIMIT 10;

SELECT COUNT(*) AS cancelled
FROM hotel_booking_10000
WHERE is_canceled = 1;

SELECT COUNT(*) AS active
FROM hotel_booking_10000
WHERE is_canceled = 0;

SELECT 
    (SUM(is_canceled) / COUNT(*)) * 100 AS cancellation_rate
FROM hotel_booking_10000;

SELECT AVG(average_daily_rate) AS average_daily_rate
FROM hotel_booking_10000;

SELECT 
    SUM(average_daily_rate * (stays_weekend_nights + stays_week_nights)) AS total_revenue
FROM hotel_booking_10000;

SELECT hotel,
SUM(average_daily_rate* (stays_weekend_nights + stays_week_nights)) AS revenue
FROM hotel_booking_10000
GROUP BY hotel;

SELECT hotel, AVG(average_daily_rate) AS average_daily_rate
FROM hotel_booking_10000
GROUP BY hotel;

SELECT 
    MONTH(arrival_date) AS month,
    COUNT(*) AS bookings
FROM hotel_booking_10000
GROUP BY month
ORDER BY month;

SELECT 
    MONTH(arrival_date) AS month,
    SUM(average_daily_rate * (stays_weekend_nights + stays_week_nights)) AS revenue
FROM hotel_booking_10000
GROUP BY month;

SELECT 
    MONTH(arrival_date) AS month,
    COUNT(*) AS bookings
FROM hotel_booking_10000
GROUP BY month
ORDER BY bookings DESC
LIMIT 1;

SELECT country,
SUM(average_daily_rate * (stays_weekend_nights + stays_week_nights)) AS revenue
FROM hotel_booking_10000
GROUP BY country
ORDER BY revenue DESC
LIMIT 5;

SELECT COUNT(*) AS high_risk
FROM hotel_booking_10000
WHERE is_canceled = 1 AND lead_time > 200;

SELECT 
CASE 
    WHEN is_canceled = 1 AND lead_time > 200 THEN 'High Risk'
    ELSE 'Normal'
END AS risk_type,
COUNT(*) AS total
FROM hotel_booking_10000
GROUP BY risk_type;

SELECT hotel,
SUM(is_canceled) AS cancellations
FROM hotel_booking_10000
GROUP BY hotel;

SELECT 
AVG(stays_weekend_nights + stays_week_nights) AS avg_stay
FROM hotel_booking_10000;

SELECT COUNT(*) AS long_stays
FROM hotel_booking_10000
WHERE (stays_weekend_nights + stays_week_nights) > 5;

SELECT is_canceled,
AVG(average_daily_rate) AS average_daily_rate
FROM hotel_booking_10000
GROUP BY is_canceled;

SELECT *,
(average_daily_rate * (stays_weekend_nights + stays_week_nights)) AS revenue
FROM hotel_booking_10000
ORDER BY revenue DESC
LIMIT 10;

SELECT 
    ROUND(SUM(is_canceled)/COUNT(*) * 100,2) AS cancellation_rate
FROM hotel_booking_10000;

SELECT 
    CASE 
        WHEN average_daily_rate < 1000 THEN 'Low Price'
        WHEN average_daily_rate  < 3000 THEN 'Medium Price'
        ELSE 'High Price'
    END AS price_category,
    AVG(is_canceled) AS cancellation_rate
FROM hotel_booking_10000
GROUP BY price_category;

SELECT market_segment,
       COUNT(*) AS total_bookings,
       SUM(is_canceled) AS cancellations
FROM hotel_booking_10000
GROUP BY market_segment
ORDER BY cancellations DESC;

