package set4

import "testing"

// TestChal25 is awesome
func TestChal25(t *testing.T) {
	str := "Try to exploit this"
	if ExploitEditAPI(str) != str {
		t.Fatal("Failed")
	}

}
