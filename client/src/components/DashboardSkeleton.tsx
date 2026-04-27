import { Skeleton } from "@/components/ui/skeleton";

const DashboardSkeleton = () => (
  <div className="space-y-8">
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <div className="lg:row-span-2 bg-card/60 border border-border/50 rounded-xl p-6 flex flex-col gap-4">
        <Skeleton className="h-4 w-24" />
        <Skeleton className="h-28 w-28 rounded-full mx-auto" />
        <Skeleton className="h-4 w-32 mx-auto" />
        <Skeleton className="h-3 w-20 mx-auto" />
      </div>
      {Array.from({ length: 6 }).map((_, i) => (
        <div key={i} className="bg-card/60 border border-border/50 rounded-xl p-5 flex flex-col gap-3">
          <div className="flex items-start justify-between">
            <Skeleton className="h-5 w-5 rounded" />
            <Skeleton className="h-5 w-16 rounded-full" />
          </div>
          <Skeleton className="h-8 w-24" />
          <Skeleton className="h-3 w-16" />
        </div>
      ))}
    </div>
    <div className="bg-card/60 border border-border/50 rounded-xl p-6 flex flex-col gap-4">
      <Skeleton className="h-4 w-40" />
      <Skeleton className="h-3 w-56" />
      <Skeleton className="h-64 w-full rounded-lg" />
    </div>
  </div>
);

export default DashboardSkeleton;
