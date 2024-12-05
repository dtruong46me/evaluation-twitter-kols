## System Architecture Design

Hệ thống sẽ được phát triển theo hướng Batch Processing trong giai đoạn đầu, tập trung vào thu thập, xử lý, phân tích, và đánh giá dữ liệu từ Twitter nhằm xác định chất lượng các tài khoản KOLs trong lĩnh vực Web3. Về lâu dài, hệ thống có thể được mở rộng để hỗ trợ Real-time Processing khi có đủ nguồn lực.

## Kiến trúc Batch Processing

:::mermaid
graph LR;
  Twitter_API --> Data_Ingestion_Layer --> Data_Lake
:::

:::mermaid
graph LR;
  Data_Lake --> Data_Processing_Layer --> Data_Warehouse
:::

:::mermaid
graph LR;
  Data_Warehouse --> Machine_Learning --> Visualization_Layer
:::

Batch Processing Architecture

**Kiến Trúc Tổng Quan**

  - Data Ingestion Layer: Thu thập dữ liệu từ Twitter API và lưu trữ vào hệ thống Data Lake.

  - Data Processing Layer: Xử lý, làm sạch, và chuẩn hóa dữ liệu.

  - Data Storage Layer: Lưu trữ dữ liệu đã xử lý vào Data Warehouse để phân tích.

  - Modeling Layer: Huấn luyện mô hình Machine Learning để đánh giá tài khoản KOLs.

  - Visualization Layer: Trực quan hóa kết quả qua dashboard.

## Kiến trúc Real-time Processing

- **Streaming Tools:** Kafka, AWS Kinesis để thu thập và xử lý dữ liệu thời gian thực.

- **Real-time Analytics:** Sử dụng Apache Flink hoặc Spark Streaming để phân tích dữ liệu trực tuyến.

- **Realtime Dashboard:** Sử dụng Grafana để hiển thị dữ liệu thời gian thực.

## System Development 

### Phase 1: Batch Processing Development

Xử lý dữ liệu lớn thu thập từ Twitter theo từng batch, nhằm phân tích, tổng hợp và lưu trữ dữ liệu phục vụ cho các mô hình Machine Learning và trực quan hóa.

### Workflow

1. **Data Collection**

    Input:

    - Danh sách KOLs liên quan đến Web3 (CSV/JSON).

    - Twitter API hoặc SNScrape để thu thập dữ liệu.

    Steps:

    - Tạo pipeline tự động thu thập dữ liệu trong khoảng thời gian cụ thể (vd: mỗi 24 giờ).

    - Dữ liệu được lưu trữ vào Data Lake (Amazon S3, Google Cloud Storage) hoặc cơ sở dữ liệu NoSQL (MongoDB, DynamoDB).

    Output:

    - Raw Data: tweet, thông tin tài khoản, tương tác.

2. **Data Preprocessing**

    Input:

    - Dữ liệu thô từ Data Lake/NoSQL.

    Quy trình:

    - Lọc bỏ các dữ liệu không liên quan hoặc trùng lặp.

    - Chuẩn hóa dữ liệu (convert định dạng thời gian, loại bỏ stopwords, mã hóa văn bản).

    - Lưu trữ dữ liệu đã xử lý vào hệ thống Data Warehouse (BigQuery, Snowflake).

    Output:

    - Dữ liệu sạch, có cấu trúc.

3. **Batch Analysis**

    Input:

    - Dữ liệu sạch từ Data Warehouse.

    Quy trình:

    - Sử dụng Spark hoặc Hadoop để phân tích các chỉ số chính như:

      - Tỷ lệ tương tác (engagement rate).
      - Tần suất đăng bài (posting frequency).
      - Hashtags liên quan đến Web3.

    - Kết quả phân tích được lưu lại để sử dụng cho các mô hình AI.

    Output:

    - Báo cáo chỉ số theo lô (JSON/Parquet).

4. **Model Training**

    Input:

    - Dữ liệu phân tích (tính năng đã trích xuất như số followers, likes, retweets).

    Quy trình:

    - Sử dụng các mô hình ML/DL (vd: Random Forest, BERT) để dự đoán mức độ ảnh hưởng và uy tín của tài khoản.

    - Lưu mô hình đã huấn luyện vào Model Registry (MLflow, S3).

    Output:

    - Mô hình sẵn sàng cho đánh giá chất lượng KOLs.

5. **Visualization**

    Input:

    - Kết quả phân tích và mô hình dự đoán.

    Quy trình:

    - Sử dụng Grafana hoặc Power BI để xây dựng dashboard.

    - Hiển thị bảng xếp hạng KOLs và các chỉ số liên quan.

    Output:

    - Dashboard cung cấp cái nhìn tổng quan về KOLs trong Web3.

### Phase 2: Real-time Processing Development
