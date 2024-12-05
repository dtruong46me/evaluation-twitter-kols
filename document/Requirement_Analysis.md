## Problem Description

Evaluation of Twitter Account Quality for KOLs in the Web3 Space. In Web3 marketing, Key Opinion Leaders (KOLs) on social media platforms like Twitter are crucial for driving trends, building communities, and shaping opinions. This project aims to develop a robust framework to assess the quality of Twitter accounts operated by KOLs in the Web3 space, providing insights into their influence, effectiveness, engagement, and credibility. 

**Requirements:**

- Identification of KOL Twitter Accounts: Compile a comprehensive list of Twitter accounts belonging to KOLs being actively involved in the Web3 space.  

- Data Collection Workflows: Develop and implement automated workflows for collecting relevant data from Twitter. 

- Deployment of Machine Learning, AI, and Deep Learning Models: Utilize advanced techniques in machine learning, artificial intelligence, and deep learning to evaluate the quality of each KOL's Twitter account.

## Requirements Analysis

Mục tiêu của dự án là phát triển một hệ thống có khả năng **đánh giá chất lượng tài khoản Twitter** của các **Key Opinion Leaders (KOLs)**, những người có sức ảnh hưởng lớn trong lĩnh vực **Web3 marketing**. Hệ thống sẽ cung cấp thông tin chuyên sâu về mức độ ảnh hưởng, mức độ uy tín, hiệu quả hoạt động, và mức độ tương tác của các tài khoản này trong việc định hình xu hướng và xây dựng cộng đồng Web3.

### Input

- Danh sách các tài khoản KOLs liên quan đến Web3.
    ```
    [
        {"username": "web3_influencer1", "id": "12345"},
        {"username": "crypto_guru", "id": "67890"}
        ...
    ]
    ```

- Các thông tin từ API của Twitter hoặc dữ liệu tự thu thập được.
    ```
    {
    "username": "web3_influencer1",
    "followers_count": 12000,
    "tweets": [
        {
            "id": "54321",
            "content": "Exploring #Web3 innovations!",
            "likes": 150,
            "retweets": 30,
            "hashtags": ["Web3", "crypto"]
        }
    ]
    }
    ```

### Output

- Bảng xếp hạng và đánh giá chất lượng tài khoản KOLs dựa trên các chỉ số sức ảnh hưởng, hiệu quả, tương tác, và uy tín.
    ```
    {
        "username": "web3_influencer1",
        "engagement_rate": 0.015,
        "influence_score": 85.6,
        "credibility_score": 92.3
    }
    ```

- Dashboard trực quan hóa các chỉ số và báo cáo chi tiết.

    |Username|Influence Score|Engagement Rate|...|
    |---|:-:|:-:|:-:|
    web3_influencer1|85.6|0.015|...
    crypto_guru|80.2|0.013|...
    ...

### Mô tả chi tiết

1. **Xác định tài khoản KOLs (Identification of KOL Twitter Accounts)**

- Thu thập và xây dựng danh sách các tài khoản Twitter của các KOLs có ảnh hưởng lớn trong lĩnh vực Web3, bao gồm các chủ đề như NFTs, Blockchain, DeFi, Metaverse, DAOs...

- Mục tiêu:
    - Đảm bảo rằng danh sách KOLs là đầy đủ, có liên quan đến Web3.
    
    - Dựa trên các tiêu chí như tần suất đăng bài, nội dung liên quan đến Web3, và mức độ phổ biến (followers, likes, retweets).

2. **Quy trình thu thập dữ liệu (Data Collection Workflows)**

- Xây dựng hệ thống tự động (automated workflows) để thu thập dữ liệu từ Twitter thông qua Twitter API hoặc các công cụ thay thế như SNScrape.

- Dữ liệu cần thu thập:

    - Thông tin tài khoản: Tên tài khoản, số lượng người theo dõi (followers), số lượng người đang theo dõi (following), ngày tạo tài khoản.

    - Nội dung tweet: Nội dung, hashtag, số lượt thích (likes), lượt chia sẻ (retweets), và lượt bình luận.

    - Tần suất hoạt động: Số lượng tweet trung bình mỗi ngày/tháng.

    - Mức độ tương tác: Tỷ lệ tương tác giữa số lượt thích, retweets với lượng followers.

- Yêu cầu kỹ thuật:

    - Hỗ trợ thu thập và xử lý Big Data, đảm bảo khả năng mở rộng (scalability).

    - Tích hợp pipeline để xử lý dữ liệu dạng batch hoặc gần real-time.

    - Lưu trữ dữ liệu trong hệ thống Big Data như Hadoop, NoSQL databases (MongoDB) hoặc Data Lakes.

3. **Ứng dụng Machine Learning/AI/Deep Learning (Model Deployment)**

- Phát triển các mô hình AI/ML/DL để đánh giá chất lượng tài khoản dựa trên các tiêu chí:

    - Sức ảnh hưởng (Influence): Mức độ lan tỏa thông tin (reach, impressions).

    - Hiệu quả (Effectiveness): Hiệu suất chiến dịch quảng cáo, nội dung tiếp cận người dùng.

    - Mức độ tương tác (Engagement): Tỷ lệ tương tác giữa likes/retweets và số followers.

    - Uy tín (Credibility): Đánh giá tài khoản dựa trên lịch sử hoạt động, chất lượng nội dung, và không có dấu hiệu spam.

- Công nghệ:

    - Sử dụng các mô hình phổ biến như Transformer-based models (BERT, RoBERTa) để phân tích nội dung.

    - Sử dụng clustering models hoặc graph analysis để đánh giá mạng lưới tương tác của các tài khoản.

4. **Hệ thống giám sát và trực quan hóa (Monitoring & Visualization)**

- Xây dựng dashboard trực quan để hiển thị các chỉ số đánh giá chất lượng tài khoản KOLs, bao gồm:

    - Biểu đồ tương tác: Tỷ lệ tương tác theo thời gian.

    - Phân tích sức ảnh hưởng: Danh sách các KOLs có ảnh hưởng cao nhất.

    - Báo cáo chi tiết: Điểm đánh giá chất lượng của từng tài khoản.
    
    - Tích hợp giám sát (monitoring) để theo dõi hiệu suất hệ thống và đảm bảo hoạt động liên tục (uptime).
