// pages/dashboard.tsx
import dynamic from 'next/dynamic';

const UserInterface = dynamic(() => import('../components/UserInterface'), { ssr: false });

export default function DashboardPage() {
  return <UserInterface backendName="flask" />;
}