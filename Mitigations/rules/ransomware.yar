rule cryptolocker
{
	strings:
		$CryptoNameSpace = "SystemSecurityCryptography"
		$CryptoFunc1 = "CryptoStream"
		$CryptoFunc2 = "ICryptoTransform"
		$CryptoFunc3 = "CryptoStreamMode"
		$CryptoFunc4 = "AesManaged"
		$CryptoFunc5 = "AesCryptoServiceProvider"
		$CryptoFunc6 = "RSACryptoServiceProvider"
		$CryptoFunc7 = "SHA1CryptoServiceProvider"
		$CryptoFunc8 = "SymmetricAlgorithm"
		$CryptoFunc9 = "AsymmetricAlgorithm"
		$CryptoFunc10 = "CreateEncryptor"
		$CryptoFunc11 = "HashAlgorithm"
		$CryptoFunc12 = "ComputeHash"
		$CryptoFunc13 = "RijndaelManaged"

	condition:
		all of them
}

rule teslacrypt
{
	strings:
		$CryptoFunc1 = {52 49 50 45 2D 4D 44 31 36 30} // RIPE-MD 160
		$CryptoFunc2 = {53 45 43 47 20 63 75 72 76 65 20 6F 76 65 72 20 61 20 32 35 36 20 62 69 74 20 70 72 69 6D 65 20 66 69 65 6C 64} // SECG curve over a 256 bit prime field
		$CryptoFunc3 = {73 65 63 70 32 35 36 6B 31} // secp256k

	condition:
		($CryptoFunc1 and $CryptoFunc2) or ($CryptoFunc1 and $CryptoFunc3)
}