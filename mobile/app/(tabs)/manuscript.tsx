import { JournalFeed } from "@/components/JournalFeed";
import { IconButton, symbols } from "@/components/IconButton";
import { PratibhaScreen } from "@/components/ui/PratibhaScreen";
import { PratibhaText, useUi } from "@/components/ui/PratibhaText";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "expo-router";
import { Pressable, View } from "react-native";

export default function ManuscriptTab() {
  const ui = useUi();
  const router = useRouter();
  const { user } = useAuth();
  return (
    <PratibhaScreen>
      <View style={{ flexDirection: "row", justifyContent: "space-between", alignItems: "flex-start" }}>
        <View style={{ flex: 1, paddingRight: 12 }}>
          <PratibhaText variant="eyebrow">My Manuscript</PratibhaText>
          <PratibhaText variant="title" style={{ marginTop: 8 }}>
            What you kept
          </PratibhaText>
          <PratibhaText variant="soft" style={{ marginTop: 8 }}>
            {user
              ? "Reflections sync with your account on the website."
              : "Reflections stay on this phone until you sign in."}
          </PratibhaText>
        </View>
        <View style={{ flexDirection: "row", gap: 16, marginTop: 4 }}>
          <IconButton name={symbols.ask} accessibilityLabel="Ask" href={"/ask" as never} />
          <IconButton name={symbols.gear} accessibilityLabel="Settings" href="/settings" />
        </View>
      </View>
      {!user ? (
        <Pressable style={[ui.buttonGhost, { marginTop: 16 }]} onPress={() => router.push("/login" as never)}>
          <PratibhaText style={ui.buttonGhostText}>Sign in to sync</PratibhaText>
        </Pressable>
      ) : null}
      <JournalFeed />
    </PratibhaScreen>
  );
}
