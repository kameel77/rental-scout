import DashboardLayout from '@/components/layout/DashboardLayout';

export default function PartnerLayout({ children }: { children: React.ReactNode }) {
    return (
        <DashboardLayout role="partner">
            {children}
        </DashboardLayout>
    );
}
