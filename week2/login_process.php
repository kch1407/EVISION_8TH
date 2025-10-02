<?php 
//db 연결 
$db_host="localhost"; 
$db_user = "root"; 
$db_pass=""; 
$db_name="my_db"; 
$db_port = 3306; 
$conn=new mysqli($db_host, $db_user, $db_pass, $db_name, $db_port);

if($conn->connect_error){
    die("데이터베이스 연결 실패: " . $conn->connect_error); // connect_error로 수정
}

//login.html에서 POST 방식으로 보낸 데이터 받기 
$username=$_POST['username']; 
$password=$_POST['password'];

// Prepared Statement 사용
$stmt = $conn->prepare("SELECT * FROM users WHERE username = ? AND password = ?");
$stmt->bind_param("ss", $username, $password); // "ss" : 문자열 2개
$stmt->execute();
$result = $stmt->get_result();

// 결과 확인 
if($result->num_rows > 0){ // num_rows로 수정
    //일치하는 사용자가 있으면(결과 행이 1개 이상이면)
    echo "<h1>로그인 성공!</h1>";
    echo "<p>'$username'님, 환영합니다.</p>";
}else{
    echo "<h1>로그인 실패</h1>";
    echo "<p>아이디 또는 비밀번호가 올바르지 않습니다.</p>";
    echo '<a href="login.html">다시 시도하기</a>';
}

//DB 연결 종료 
$conn->close(); 
?>