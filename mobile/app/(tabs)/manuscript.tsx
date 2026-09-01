import { JournalFeed } from "@/components/JournalFeed";
import { IconButton, symbols } from "@/components/IconButton";
import { PratibhaScreen } from "@/components/ui/PratibhaScreen";
import { PratibhaText } from "@/components/ui/PratibhaText";
import { View } from "react-native";

export default function ManuscriptTab() {
  return (
    <PratibhaScreen>
      <View style={{ flexDirection: "row", justifyContent: "space-between", alignItems: "flex-start" }}>
        <View style={{ flex: 1, paddingRight: 12 }}>
          <PratibhaText variant="eyebrow">Mine</PratibhaText>
          <PratibhaText variant="title" style={{ marginTop: 8 }}>
            What you kept
          </PratibhaText>
          <PratibhaText variant="soft" style={{ marginTop: 8 }}>
            Reflections and saved replies, kept on this phone.
          </PratibhaText>
        </View>
        <View style={{ flexDirection: "row", gap: 16, marginTop: 4 }}>
          <IconButton name={symbols.ask} accessibilityLabel="Ask" href={"/ask" as never} />
          <IconButton name={symbols.gear} accessibilityLabel="Settings" href="/settings" />
        </View>
      </View>
      <JournalFeed />
    </PratibhaScreen>
  );
}
