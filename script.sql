DROP TABLE IF EXISTS Posts;

CREATE TABLE Posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,       -- Unique identifier for each entry
    avatar_url TEXT,                            -- URL or path to an avatar image
    name TEXT NOT NULL,                         -- Name of the person/entity
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Date and time of creation
                                                -- Stored as TEXT in ISO8601 format (YYYY-MM-DD HH:MM:SS)
    description TEXT,                           -- A textual description
    location TEXT,                              -- Location as a string (e.g., "New York, USA", "Room 101")
    image_url TEXT                              -- URL or path to a main image
);

INSERT INTO Posts (avatar_url, name, created_at, description, location, image_url) VALUES
(
    'assets/avatar.png',
    'Nguyễn Văn An',
    '2024-03-10 23:55:00',
    'Trận lũ quét kinh hoàng tại Sa Pa, cuốn trôi nhiều nhà cửa và gây thiệt hại nặng nề về hoa màu. Mọi người đang khẩn trương sơ tán.',
    'Sa Pa, Lào Cai',
    'assets/flood.jpg'
),
(
    'assets/avatar.png',
    'Trần Thị Bích',
    '2024-03-11 12:30:15',
    'Hạn hán kéo dài ở Đồng Tháp khiến kênh rạch khô cạn, đồng ruộng nứt nẻ. Nông dân đối mặt với nguy cơ mất trắng mùa màng.',
    'Đồng Tháp',
    'assets/drought.jpg'
),
(
    'assets/avatar.png',
    'Lê Văn Cường',
    '2024-03-09 08:15:45',
    'Sạt lở đất nghiêm trọng xảy ra tại Mộc Châu sau những ngày mưa lớn, chia cắt nhiều tuyến đường và cô lập các bản làng.',
    'Tân Lập, Mộc Châu, Sơn La',
    'assets/earthquake.jpg'
);

