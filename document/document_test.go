package document

import "testing"

func TestHello(t *testing.T) {
	assertEqual := func(t *testing.T, got, want string) {
		t.Helper()
		if got != want {
			t.Errorf("'%s' is not '%s'", got, want)
		}
	}

	t.Run("", func(t *testing.T) {
		doc := Document{"/content/pages/home.yaml"}
		got := doc.podPath
		want := "/content/pages/home.yaml"
		assertEqual(t, got, want)
	})
}
