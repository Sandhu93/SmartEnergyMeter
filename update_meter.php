<?php
if($_SERVER["REQUEST_METHOD"]=="POST")
{
	require 'meter_connection.php';
	createstudent();
}

function createstudent()
{
	global $connect;
	$recharge_amount = $_POST["recharge"];
	$mquery = "SELECT balance_amount FROM user_info WHERE user_id=1;";
	$result = mysqli_query($connect,$mquery);
	$number_of_rows = mysqli_num_rows($result);
	if($number_of_rows > 0)
	{
		while($row=mysqli_fetch_assoc($result))
		{
			$temp =$row['balance_amount'];
		
		}
	}
		
	$balance = $temp + $recharge_amount;
	$energy = $balance;

	echo $balance;	
	
	$query = "UPDATE user_info SET balance_amount='$balance',energy_remaining='$energy' WHERE user_id=1;";
	
	mysqli_query($connect,$query) or die (mysqli_error($connect));
	mysqli_close($connect);
}

?>