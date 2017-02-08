SET @belogorsk='белогорск';
SET @sudak='судак';
SET @feodosia='феодосия';
SET @simf='симф';

INSERT INTO calendar (id, name) VALUES (5, @belogorsk) ON DUPLICATE KEY UPDATE name = @belogorsk;
INSERT INTO calendar (id, name) VALUES (17, @sudak) ON DUPLICATE KEY UPDATE name = @sudak;
INSERT INTO calendar (id, name) VALUES (34, @feodosia) ON DUPLICATE KEY UPDATE name = @feodosia;

-- устанавливает время работы отделения @belogorsk с 9 до 19
UPDATE schedule
	SET time_begin_1='09:00:00',
		time_end_1='19:00:00',
        time_begin_2='09:00:00',
		time_end_2='19:00:00',
        time_begin_3='09:00:00',
		time_end_3='19:00:00',
        time_begin_4='09:00:00',
		time_end_4='19:00:00',
        time_begin_5='09:00:00',
		time_end_5='19:00:00',
        time_begin_6='09:00:00',
		time_end_6='19:00:00',
        time_begin_7='09:00:00',
		time_end_7='19:00:00'
	WHERE schedule.name = @belogorsk OR schedule.name = @sudak OR schedule.name=@feodosia;
    
-- удаляет все выходные для @belogorsk
DELETE calendar_out_days
	FROM calendar_out_days 
		INNER JOIN calendar 
		ON calendar_out_days.calendar_id = calendar.id 
	    WHERE calendar.name = @belogorsk OR calendar.name = @sudak OR calendar.name=@feodosia;

-- устанавливает время услуг
UPDATE standards SET next_opening_date = CURRENT_DATE() + INTERVAL 10 DAY;

-- устанавливает время услуг
UPDATE services SET duration = 25 WHERE name LIKE '%постановка%';
UPDATE services SET duration = 40
	WHERE (name LIKE '%един%' OR name LIKE '%перех%') AND aditional_duration != 0;
UPDATE services SET duration = 35
	WHERE (name LIKE '%един%' OR name LIKE '%перех%') AND aditional_duration = 0;

-- устанавливает дату окончания предварительной записи
UPDATE department
	SET finish_advance_date = CURRENT_DATE() + INTERVAL 2 DAY
	WHERE name LIKE concat("%",@belogorsk,"%")
	    OR name LIKE concat("%",@sudak,"%")
	    OR name LIKE concat("%",@feodosia,"%");

UPDATE department
	SET finish_advance_date = CURRENT_DATE() - INTERVAL 1 DAY
	WHERE name LIKE concat("%",@simf,"%");

UPDATE department SET calendar_id = 5 WHERE name LIKE concat("%",@belogorsk,"%");
UPDATE department SET calendar_id = 17 WHERE name LIKE concat("%",@sudak,"%");
UPDATE department SET calendar_id = 34 WHERE name LIKE concat("%",@feodosia,"%");

-- устанавливает процент времени для физ и юр лиц
UPDATE service_groups SET advance_time_percent = 0.7 WHERE id=1;
UPDATE service_groups SET advance_time_percent = 0.3 WHERE id=2;

-- удаляет всех предварительно записанных для @belogorsk и @sudak
DELETE FROM advance;
DELETE FROM logs;
DELETE FROM history;

-- удаляет тестового пользователя для проверки импорта регистраторов
DELETE FROM acl_users WHERE name not like '7990%';
DELETE FROM customers WHERE mobile_phone not like '7990%';

-- макс. время опоздания = 5 минут, макс. время до назначенного = 60 минут.
UPDATE standards SET wait_max_advance=5, before_max_advance=60;

-- перерыв
INSERT INTO break (id, from_time, to_time, duration)
	VALUES (3, '15:00', '16:00', '60')
	ON DUPLICATE KEY UPDATE from_time = '15:00', to_time = '16:00', duration = '60';

UPDATE schedule
	SET breaks_id1=3,
        breaks_id2=3,
        breaks_id3=3,
        breaks_id4=3,
        breaks_id5=3,
        breaks_id6=3,
        breaks_id7=3
	WHERE schedule.name IN (@belogorsk, @sudak, @feodosia);
