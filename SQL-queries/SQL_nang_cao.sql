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


/****** 
tạo tập dữ liệu về các trận đấu được xếp hạng theo đó trung bình các giải đấu ghi được nhiều bàn thắng nhất trong một trận đấu. 
******/
SELECT 
	-- Select the league id and average goals scored
	match_id,
    AVG(home_team_goals + away_team_goals) AS avg_goals,
    -- Rank each league according to the average goals
    RANK() OVER(ORDER BY AVG(home_team_goals + away_team_goals)) AS league_rank
FROM [ap_football].[dbo].[world_cup_matches]
WHERE year = '2002'
GROUP BY match_id
-- Order the query by the rank you created
ORDER BY league_rank;



/****** 
CASE
******/

-- Xác định thắng, thua hoặc hòa trên sân nhà
SELECT 
	-- Chọn ngày của trận đấu
	match_date,
	CASE WHEN full_time_home_team_goals > full_time_away_team_goals THEN 'Home win ^^'
         WHEN full_time_home_team_goals < full_time_away_team_goals THEN 'Home loss TT' 
         ELSE 'Tie' END AS outcome
FROM [ap_football].[dbo].[national_leagues_2000_2022];

---------------------
/***
Sử dụng quốc gia và bảng đấu để xác định tổng số trận thắng của đội chủ nhà ở mỗi quốc gia trong các mùa giải 2012-2013, 2013-2014 và 2014-2015. 
***/

SELECT 
	home_team AS country,
    -- Tính tổng các kỷ lục trong mỗi mùa giải mà đội nhà giành được 
	SUM(CASE WHEN season = '2012-2013' AND full_time_home_team_goals > full_time_away_team_goals 
        THEN 1 ELSE 0 END) AS matches_2012_2013, --- chuyển các giá trị này thành 1 và 0 trước khi tính tổng
	SUM(CASE WHEN season = '2013-2014' AND full_time_home_team_goals > full_time_away_team_goals 
        THEN 1 ELSE 0 END) AS matches_2013_2014,
	SUM(CASE WHEN season = '2014-2015' AND full_time_home_team_goals > full_time_away_team_goals 
        THEN 1 ELSE 0 END) AS matches_2014_2015
FROM [ap_football].[dbo].[national_leagues_2000_2022]
-- Nhóm theo bí danh tên quốc gia 
GROUP BY home_team;
