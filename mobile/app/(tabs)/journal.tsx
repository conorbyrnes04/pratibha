import { Redirect } from "expo-router";

export default function JournalTabRedirect() {
  return <Redirect href={"/(tabs)/manuscript" as never} />;
}
