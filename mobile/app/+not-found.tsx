import { Link, Stack } from "expo-router";
import { Pressable } from "react-native";

import { PratibhaScreen } from "@/components/ui/PratibhaScreen";
import { PratibhaText, ui } from "@/components/ui/PratibhaText";

export default function NotFoundScreen() {
  return (
    <>
      <Stack.Screen options={{ title: "Not found" }} />
      <PratibhaScreen scroll={false} contentStyle={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
        <PratibhaText variant="eyebrow">Lost passage</PratibhaText>
        <PratibhaText variant="title" style={{ marginTop: 12, textAlign: "center" }}>
          This screen doesn&apos;t exist
        </PratibhaText>
        <PratibhaText variant="soft" style={{ marginTop: 12, textAlign: "center", maxWidth: 280 }}>
          The route you followed isn&apos;t part of the Pratibha app yet.
        </PratibhaText>
        <Link href="/" asChild>
          <Pressable style={[ui.button, { marginTop: 24 }]}>
            <PratibhaText style={ui.buttonText}>Return home</PratibhaText>
          </Pressable>
        </Link>
      </PratibhaScreen>
    </>
  );
}
