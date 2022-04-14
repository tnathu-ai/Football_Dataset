-- SỬ DỤNG SQL LÀM SẠCH DỮ LIỆU

/****** 
Sử dụng LEFT để kéo một số ký tự nhất định từ phía bên trái của một chuỗi và trình bày chúng dưới dạng một chuỗi riêng biệt. LEFT(string, number of characters).
RIGHT làm điều tương tự, nhưng từ phía bên phải
******/
SET SHOWPLAN_XML ON
SELECT [year]
      ,[round_id]
      ,[match_id]
      ,[date_time]
      ,LEFT([date_time], 10) AS cleaned_date
	  ,RIGHT([date_time], 17) AS cleaned_time
	  ,RIGHT([date_time], LEN([date_time]) - 11) AS cleaned_time_using_LEN -- LEN trả về chiều dài của chuỗi
FROM [ap_football].[dbo].[world_cup_matches];


/****** 
Hàm TRIM được sử dụng để loại bỏ các ký tự từ đầu và cuối của một chuỗi:
******/
SELECT TRIM('     SQL Vietnam     ') AS TrimmedString;

/****** 
Hàm CHARINDEX () trả về vị trí của ký tự 'olymp' (không phân biệt chữ hoa chữ thường) nơi nó xuất hiện lần đầu trong trường 'stadium':
******/
SELECT [stadium]
       ,CHARINDEX('olymp', [stadium]) AS olymp_position
FROM [ap_football].[dbo].[world_cup_matches]


/****** 
Trích xuất 5 ký tự từ cột "stadium", bắt đầu ở vị trí 1:
******/
SELECT [stadium], SUBSTRING([stadium], 1, 5) AS ExtractString
FROM [ap_football].[dbo].[world_cup_matches];


/****** 
trả về tất cả các hàng có giá trị penalty_home không bị thiếu
******/
SELECT [year]
      ,[round_id]
      ,[match_id]
      ,[home_team_code]
      ,[home_team_name]
      ,[away_team_code]
      ,[penalty_home]
FROM [ap_football].[dbo].[world_cup_matches]
WHERE penalty_home IS NOT NULL;



/****** 
Thay thế giá trị còn thiếu
******/
SELECT [year]
      ,[round_id]
      ,[match_id]
      ,[home_team_code], ISNULL(home_team_code, home_team_name) AS home_team	-- kiểm tra home_team_code có giá trị rỗng hay không và thay thế giá trị rỗng với giá trị bên home_team_name
      ,[home_team_name]
      ,[penalty_home]
FROM [ap_football].[dbo].[world_cup_matches]
WHERE home_team_code IS NULL;	    ---trả về giá trị rỗng cho home_team_code



/****** 
SUM(attendance), trông rất giống với bất kỳ chức năng aggregation khác. 
Thêm OVER chỉ định nó như một chức năng cửa sổ. 
Bạn có thể đọc tổng hợp ở trên là "lấy tổng của attendance toàn bộ tập kết quả, theo thứ tự date_time. 
Nếu bạn muốn thu hẹp cửa sổ từ toàn bộ tập dữ liệu thành các nhóm riêng lẻ theo tên của đội nhà trong tập dữ liệu, bạn có thể sử dụng PARTITION BY để làm như vậy:
******/
SELECT [date_time]
      ,[attendance]
	  ,SUM([attendance]) OVER (PARTITION BY home_team_name ORDER BY [date_time]) AS running_total
  FROM [ap_football].[dbo].[world_cup_matches]