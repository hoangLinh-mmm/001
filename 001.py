import streamlit as st
from sklearn.linear_model import LinearRegression
import feedparser

st.sidebar.title(" Danh sách các nghệ sĩ ")
selected_artist = st.sidebar.radio("Chọn nghệ sĩ", ["Đen Vâu", "Hà Anh Tuấn", "Sơn Tùng M-TP"])
videos = {
    "Đen Vâu": [
        ("Bữa ăn cho em", "https://www.youtube.com/watch?v=ukHK1GVyr0I"),
        ("Mang tiền về cho mẹ", "https://www.youtube.com/watch?v=UVbv-PJXm14"),
        ("Trời hôm nay nhiều mây cực!", "https://www.youtube.com/watch?v=MBaF0l-PcRY"),
        ("Hai triệu năm", "https://www.youtube.com/watch?v=LSMDNL4n0kM")
    ],
    "Hà Anh Tuấn": [
        ("Tuyết rơi mùa hè", "https://www.youtube.com/watch?v=pTh3KCD7Euc"),
        ("Nước ngoài", "https://www.youtube.com/watch?v=pU3O9Lnp-Z0"),
        ("Tháng tư là lời nói dối của em", "https://www.youtube.com/watch?v=UCXao7aTDQM"),
        ("Xuân thì", "https://www.youtube.com/watch?v=3s1r_g_jXNs")
    ],
    "Sơn Tùng M-TP": [
        ("Lạc trôi", "https://www.youtube.com/watch?v=Llw9Q6akRo4"),
        ("Chúng ta không thuộc về nhau", "https://www.youtube.com/watch?v=qGRU3sRbaYw"),
        ("Muộn rồi mà sao còn", "https://www.youtube.com/watch?v=xypzmu5mMPY"),
        ("Hãy trao cho anh", "https://www.youtube.com/watch?v=knW7-x7Y7RE")
    ]    
}
st.title(" Ứng dụng giải trí và sức khỏe ")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["MV yêu thích", "Dự đoán giờ đi ngủ", "Đọc báo", "Giá vàng mới nhất", "Tính chỉ số BMI"])
with tab1:
    st.header(f"Các bài hát {selected_artist}")
    for title, url in videos[selected_artist]:
        st.subheader(title)
        st.video(url)
with tab2:
    from sklearn.linear_model import LinearRegression
    st.title("😀 Dự đoán số giờ ngủ cần thiết ")
    #Dữ liệu mẫu: [tuổi, mực độ vận động (1-10), thời gian dùng màn hình(giờ)]
    x = [
        [10, 8, 1],
        [20, 6, 5],
        [25, 3, 8],
        [30, 2, 6],
        [50, 2, 2],
        [15, 9, 2],
        [40, 4, 3]
    ]
    y = [10, 8, 6, 6, 5, 7, 9.5] # giờ ngủ được khuyên
    #Huấn luyện mô hình
    model = LinearRegression()
    model.fit(x, y)
    #giao diện người dùng
    st.write("Nhập thông tin của bạn: ")

    age = st.number_input("Tuổi của bạn ", min_value=5, max_value=100, value=25)
    activity = st.slider("Mức độ hoạt động thể chất (1 = ít, 10 = rất nắng động)", 1, 10, 5)
    screen_time = st.number_input("Thời gian dùng màn hình mỗi ngày(giờ)", min_value=0, max_value=24, value=6)

    if st.button("🥱 Dự đoán giờ đi ngủ "):
        input_data = [[age, activity, screen_time]]
        result = model.predict(input_data)[0]
        st.success(f"Bạn nên ngủ khoảng {result:.1f} giờ mỗi đêm")

        #Gợi ý thêm
        if result < 6.5:
            st.warning("Có thể bạn cần nghỉ ngơi nhiều hơn để cái thiện sức khỏe.")
        elif result > 9:
            st.info("Bạn có thể đang cận động nhiều-Ngủ đủ rất quan trọng để hồi phục cơ thể")
        else:
            st.success("Lượng ngủ lý tưởng! Hãy giữ thói quen tốt nhé. ")
with tab3:
    st.header(" Tin mới nhất từ VnExpress ")
    feed = feedparser.parse("https://vnexpress.net/rss/tin-moi-nhat.rss")
    for entry in feed.entries[:5]:
        st.subheader(entry.title)
        st.write(entry.published)
        st.write(entry.link)
with tab4:
    st.header(" Cập nhật giá vàng từ Vietnamnet ")
    feed = feedparser.parse("https://vietnamnet.vn/rss/kinh-doanh.rss")
    gold_news = [entry for entry in feed.entries if "vàng" in entry.title.lower() or "giá vàng" in entry.summary.lower()]
    if gold_news:
        for entry in gold_news[:5]:
            st.subheader(entry.title)
            st.write(entry.published)
            st.write(entry.link)
        else:
            st.warning("Không tìm thấy bản tin giá vàng gần nhất")
with tab5:
    st.header("Kiểm tra chỉ số BMI của bạn")
    can_nang = st.number_input("Nhập cân nặng của bạn (kg): ", min_value=10.0, max_value=200.0, value=60.0, step=0.1)
    chieu_cao = st.number_input("Nhập chiều cao của bạn (m)", min_value=1.0, max_value=2.5, value=1.7, step=0.01)
    if st.button(" Tính BMI "):
        bmi = can_nang / (chieu_cao ** 2)
        st.success(f"Chỉ số BMI của bạn là: {bmi: .2f}")

        if bmi < 18.5:
            st.warning("Bạn đang bị thiếu cân vì vậy bạn nên ăn uống đầy đủ và nhiều dinh dưỡng hơn")
        elif 18.5 <= bmi < 25:
            st.info("Bạn có cân nặng bình thường. Hãy tiếp tục duy trì lối sống lành mạnh")
        elif 25 <= bmi < 30:
            st.warning(" Bạn đang thừa cân. Nên cân đối chế dộ ăn và tập thể dục")
        else:
            st.error("Bạn đang béo phì. Nên gặp chuyên gia dinh dưỡng hoặc bác sĩ để được tư vấn")
