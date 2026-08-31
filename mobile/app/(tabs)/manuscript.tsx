import { PratibhaScreen } from "@/components/ui/PratibhaScreen";
import { PratibhaText, ui } from "@/components/ui/PratibhaText";
import { Link } from "expo-router";
import { Pressable, View } from "react-native";

export default function ManuscriptTab() {
  return (
    <PratibhaScreen>
      <PratibhaText variant="eyebrow">Mine</PratibhaText>
      <PratibhaText variant="title" style={{ marginTop: 8 }}>
        My manuscript
      </PratibhaText>
      <PratibhaText variant="soft" style={{ marginTop: 16, fontSize: 16, lineHeight: 24 }}>
        Keep verses as a chapbook. Compose and publish the folio on the web; this tab is the same
        seat as My Manuscript there.
      </PratibhaText>
      <View style={[ui.card, { marginTop: 20 }]}>
        <PratibhaText variant="label">The walk</PratibhaText>
        <PratibhaText variant="heading" style={{ marginTop: 8, fontSize: 20 }}>
          Today → Path → Library → Mine
        </PratibhaText>
        <PratibhaText variant="soft" style={{ marginTop: 8 }}>
          Finish a gate on Today. The trail names tomorrow. Library holds the house. Mine gathers
          what you keep.
        </PratibhaText>
      </View>
      <Link href="/(tabs)/" asChild>
        <Pressable style={[ui.button, { marginTop: 20 }]}>
          <PratibhaText style={ui.buttonText}>Return to Today</PratibhaText>
        </Pressable>
      </Link>
    </PratibhaScreen>
  );
}
