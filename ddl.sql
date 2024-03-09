// КОД ДЛЯ СОЗДАНИЯ ТАБЛИЦЫ
CREATE TABLE IF NOT EXISTS page_metrics (
    url String,
    lcp Float64,
    tbt Float64,
    date Date,
    PRIMARY KEY (url, date)
) ENGINE = MergeTree()
ORDER BY (url, date);
