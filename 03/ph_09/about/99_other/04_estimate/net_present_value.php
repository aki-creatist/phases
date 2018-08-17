<?php
$err_msg1 = '';
$err_msg2 = '';
$aa = (isset( $_POST['aa']) === true) ? htmlspecialchars($_POST['aa']) : '';
$bb = (isset( $_POST['bb']) === true) ? htmlspecialchars($_POST['bb']) : '';

if (isset($_POST["send"]) ===  true) {

    if ($aa === '') $err_msg1 = '年を入力してください。';
    if ($bb === '') $err_msg2 = '金額を入力してください。';

    if ($err_msg1 === '' && $err_msg2 === '') {
        $num = 1;
        for ($i = 1; $i < $aa; $i++) {
            $num = $num * 1.1;
        }
        $cc = $bb/$num;
    }
}
?>

<div style="width:40%; float:left;">
    <form method="POST" action="#npv" style="width:80%">
        年：<input type="text" size="3" name="aa" value="<?=$aa?>" />年目<br>
        <?php echo $err_msg1; echo round($num, 2) . "<br>";?><br />

        金額：<input type="text"  size="3" name="bb" value="<?=$bb?>" /><br>
        <?php echo $err_msg2; echo round($cc,2) . "円";?><br />

        <input type="submit" name="send" value="計算" />
    </form>
</div>