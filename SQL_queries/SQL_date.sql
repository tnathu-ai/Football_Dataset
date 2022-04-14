/****** chọn các bản ghi có date_time là '1930-07-17 14:45:00.0000000' từ bảng dưới.  ******/
SELECT *
FROM [ap_football].[dbo].[world_cup_matches]
WHERE date_time='1930-07-17 14:45:00.0000000';


/****** chọn các bản ghi có date_time là '1930-07-17' từ bảng dưới.  Sử dụng truy vấn chỉ tìm kiếm các ngày không có phần thời gian. 
=> không nhận được kết quả
******/
SELECT *
FROM [ap_football].[dbo].[world_cup_matches]
WHERE date_time='1930-07-17';