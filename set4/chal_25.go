package set4

import (
	"crypto/aes"
	"encoding/binary"
	"errors"
	"fmt"
)

// func main() {
// fmt.Println("[+] Starting...")
// pt := []byte("This has to be !")
// secret := "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
// key := []byte("YELLOW SUBMARINE")
// nonce := uint64(0)

// encryptAesCtr(pt, key, nonce)
// ct, err := aesEcbEncrypt([]byte(pt), []byte(key))
// if err != nil {
// 	fmt.Println(err.Error())
// }

// ptRecovered, err := aesEcbDecrypt(ct, []byte(key))
// if err != nil {
// 	fmt.Println(err.Error())
// }

// if bytes.Compare(ptRecovered, []byte(pt)) != 0 {
// 	panic("Errr")
// }
/*
	secretDecoded, err := base64.StdEncoding.DecodeString(secret)
	if err != nil {
		panic("Failed to decode")
	}
	ct := encryptAesCtr(secretDecoded, key, nonce)
	fmt.Printf("'%s'\n", string(ct))
	secretBack := encryptAesCtr(ct, key, nonce)
	if bytes.Compare(secretDecoded, secretBack) != 0 {
		panic("Err")
	}

	test := "aabbbAAAAABBBBBBBBBBBBBBBBBDDDDDDDD"
	ct = encryptAesCtr([]byte(test), key, nonce)
	newCt, err := edit(ct, key, 10, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
	if err != nil {
		panic("Failed to edit: " + err.Error())
	}
	editStr := decryptAesCtr(newCt, key, nonce)
	fmt.Println(string(test))
	fmt.Println(string(editStr))
*/
// secretDecoded, err := base64.StdEncoding.DecodeString(secret)
// if err != nil {
// 	panic("Failed to decode")
// }

// ct := encryptAesCtr([]byte("Hello world"), mainKey, mainNonce)
// exploitEdit(ct)

// }

func min(a, b uint) uint {
	if a > b {
		return b
	}
	return a
}

func edit(ctOrig []byte, key []byte, offset uint, newText string) ([]byte, error) {
	ct := make([]byte, len(ctOrig))
	if int(offset) > len(ct) {
		return []byte{}, errors.New("Invalid offset")
	}

	newTextLen := uint(len(newText))
	firstBlock := offset / 16
	firstBlockOff := offset % 16
	lastBlock := (offset + newTextLen) / 16
	if (offset+newTextLen)%16 != 0 {
		lastBlock++
	}
	// lastBlockOff := (offset + newTextLen) % 16

	editCt := ct[firstBlock*16 : min(uint(len(ct)), lastBlock*16)]
	origPt := decryptAesCtr(editCt, key, uint64(firstBlock))

	// fmt.Printf("Original string: %s\n", origPt)

	editPt := append(origPt[:firstBlockOff], []byte(newText)...)
	if len(editPt) < len(origPt) {
		editPt = append(editPt, origPt[len(editPt):]...)
	}

	// fmt.Printf("New string: %s\n", editPt)
	newCt := encryptAesCtr(editPt, key, uint64(firstBlock))

	finalCt := append(ct[:firstBlock*16], newCt...)
	if len(finalCt) < len(ct) {
		finalCt = append(finalCt, ct[len(finalCt):]...)
	}
	return finalCt, nil
}

func encryptAesCtr(ptBytes []byte, keyBytes []byte, nonce uint64) []byte {
	nonceBytes := make([]byte, 8)
	binary.PutUvarint(nonceBytes, nonce)
	ctrBytes := make([]byte, 8)

	ctBytes := make([]byte, len(ptBytes))

	for i := 0; i < len(ptBytes); i += 16 {
		binary.PutUvarint(ctrBytes, uint64(i)/16)

		xorKey, err := aesEcbEncrypt(append(nonceBytes, ctrBytes...), keyBytes)

		if err != nil {
			fmt.Println(err.Error())
			panic("[-] Aborting")
		}

		xor(ctBytes[i:], xorKey, ptBytes[i:])
		// fmt.Println(i, binary.PutUvarint(aesKey, nonce), aesKey)
		// fmt.Println(append(nonceBytes, ctrBytes...))
	}

	return ctBytes
}

var decryptAesCtr = encryptAesCtr

func xor(dst []byte, src []byte, key []byte) {
	length := len(src)
	if length > len(key) {
		length = len(key)
	}
	for i := 0; i < length; i++ {
		dst[i] = src[i] ^ key[i]
	}
}

func aesEcbEncrypt(pt []byte, key []byte) ([]byte, error) {
	if (len(pt) % 16) != 0 {
		return []byte{}, errors.New("Invalid size of plaintext")
	}

	cipher, err := aes.NewCipher(key)
	if err != nil {
		return []byte{}, errors.New("Failed to create AES cipher")
	}

	ct := make([]byte, len(pt))

	for i := 0; i < len(pt); i += 16 {
		bb := i
		be := i + 16
		cipher.Encrypt(ct[bb:be], pt[bb:be])
	}

	return ct, nil
}

func aesEcbDecrypt(ct []byte, key []byte) ([]byte, error) {
	if (len(ct) % 16) != 0 {
		return []byte{}, errors.New("Invalid size of plaintext")
	}

	cipher, err := aes.NewCipher(key)
	if err != nil {
		return []byte{}, errors.New("Failed to create AES cipher")
	}

	pt := make([]byte, len(ct))

	for i := 0; i < len(ct); i += 16 {
		bb := i * 16
		be := i*16 + 16
		cipher.Decrypt(pt[bb:], ct[bb:be])
	}

	return pt, nil
}

// ExploitEditAPI is required
func ExploitEditAPI(pt string) string {
	key := []byte("YELLOW SUBMARINE")
	nonce := uint64(0)
	fmt.Println("Ok")
	ct := encryptAesCtr([]byte(pt), key, nonce)
	return exploitEdit(ct)
}

func editAPI(ct []byte, offset uint, newText string) ([]byte, error) {
	mainKey := []byte("YELLOW SUBMARINE")
	return edit(ct, mainKey, offset, newText)
}

func exploitEdit(origCt []byte) string {
	plaintext := ""
	for i := range origCt {
		if len(plaintext) != i {
			fmt.Printf("%d, %s\n", i, plaintext)
		}
		for j := 0; j < 128; j++ {
			res, _ := editAPI(origCt, uint(i), string(j))

			if res[i] == origCt[i] {
				plaintext += string(j)
				break
			}
		}
	}
	return plaintext
}
