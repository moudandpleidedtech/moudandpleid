"use client";

import CertificateReveal from "@/components/Game/CertificateReveal";
import { useRouter } from "next/navigation";

export default function CertificadoPage() {
  const router = useRouter();
  return <CertificateReveal onClose={() => router.push("/hub")} />;
}
