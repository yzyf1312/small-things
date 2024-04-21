function genPassword(str, hash) {
    for (var byteIndex = str.length - 1; byteIndex >= 0; byteIndex--) {
        hash = f1(hash, str.charCodeAt(byteIndex), 0x105C3);
    }
    var n1 = 0;
    while (f1(f1(hash, n1 & 0xFF, 0x105C3), n1 >> 8, 0x105C3) !== 0xA5B6) {
        if (++n1 >= 0xFFFF) {
            return "Error";
        }
    }
    n1 = Math.floor(((n1 + 0x72FA) & 0xFFFF) * 99999.0 / 0xFFFF);
    var n1str = ("0000" + n1.toString(10)).slice(-5);
    var temp = parseInt(n1str.slice(0, -3) + n1str.slice(-2) + n1str.slice(-3, -2), 10);
    temp = Math.ceil((temp / 99999.0) * 0xFFFF);
    temp = f1(f1(0, temp & 0xFF, 0x1064B), temp >> 8, 0x1064B);
    for (byteIndex = str.length - 1; byteIndex >= 0; byteIndex--) {
        temp = f1(temp, str.charCodeAt(byteIndex), 0x1064B);
    }
    var n2 = 0;
    while (f1(f1(temp, n2 & 0xFF, 0x1064B), n2 >> 8, 0x1064B) !== 0xA5B6) {
        if (++n2 >= 0xFFFF) {
            return "Error";
        }
    }
    n2 = Math.floor((n2 & 0xFFFF) * 99999.0 / 0xFFFF);
    var n2str = ("0000" + n2.toString(10)).slice(-5);
    return n2str[3] + n1str[3] + n1str[1] + n1str[0] + "-"
        + n2str[4] + n1str[2] + n2str[0] + "-"
        + n2str[2] + n1str[4] + n2str[1] + "::1";
}



function checkMathId(s) {
    if (s.length != 16)// 输入的MathId长度不是16时报错
        return false;
    for (let i = 0; i < s.length; i++) {
        if (i === 4 || i === 10) {
            if (s[i] !== "-")// 输入的MathId分隔符不符合规范时报错
                return false;
        } else {
            if ("0123456789".search(s[i]) < 0)// 输入的MathId包含非数字字符时报错
                return false;
        }
    }
    return true;
}

function genActivationKey() {
    s = "";
    for (let i = 0; i < 14; i++) {// 执行14遍循环
        s += Math.floor(Math.random() * 10);// 随机生成一个一位数并附加到变量s的结尾
        if (i === 3 || i === 7)
            s += "-";// 在第4位和第8位设置分隔符"-"
    }
    return s;
}

document.getElementById("generate").addEventListener("click", function () {
    var mathId = document.getElementById("mathId").value.trim();// 获取输入的mathId
    // 检查输入的mathId是否符合规范
    if (!checkMathId(mathId)) {
        document.getElementById("result").innerText = "Bad MathID!";
    } else {// 如果mathId符合规范则继续执行
        var activationKey = genActivationKey();// 设定激活码
        var magicNumbers;
        var software = document.querySelector("input[name=product]:checked").value;// 检查希望激活的产品类型; mma12:Mathematica 11/12; mma13:Mathematica 13; sm12:System Modeler 12/13
        if (software === "mma12" || software === "mma13") {
            magicNumbers = [10690, 12251, 17649, 24816, 33360, 35944, 36412, 42041, 42635, 44011, 53799, 56181, 58536, 59222, 61041];
        } else if (software === "sm12") {
            magicNumbers = [4912, 4961, 22384, 24968, 30046, 31889, 42446, 43787, 48967, 61182, 62774];
        } else {
            document.getElementById("result").innerHTML = `<p>Unknown software suite: ${software}.</p>`;
            return;
        }
        var magicNumber = magicNumbers[Math.floor(Math.random() * magicNumbers.length)]// 在magicNumbers里面随机挑选一个数字给magicNumber
        var password = genPassword(mathId + "$1&" + activationKey, magicNumber);
        document.getElementById("result").innerHTML = `
        <p>
        <b>Activation Key</b>: ${activationKey}
        <br>
        <b>Password</b>: ${password}
        </p>
        <p>Thanks for using! Please consider purchasing the software if you find it helpful to you. We support genuine software.</p>
        `;
    }
});