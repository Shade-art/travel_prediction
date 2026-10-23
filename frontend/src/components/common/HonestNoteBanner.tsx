import React from 'react';
import { Info, MapPin } from 'lucide-react';

export const HonestNoteBanner: React.FC<{ compact?: boolean }> = ({ compact = false }) => {
  return (
    <div className={`bg-slate-900/90 border border-amber-500/30 rounded-xl ${compact ? 'p-3' : 'p-4'} flex items-start gap-3 shadow-sm`}>
      <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400 border border-amber-500/20 shrink-0">
        <MapPin className="w-4 h-4" />
      </div>
      <div className="text-xs text-slate-300 leading-relaxed">
        <div className="flex items-center gap-1.5 font-semibold text-amber-300 mb-1">
          <Info className="w-3.5 h-3.5" />
          <span>Transit Domain Integrity Note: Catchment Zone vs Fixed Route Analysis</span>
        </div>
        <p>
          Unlike scheduled subways or municipal buses with fixed corridors, NYC Yellow and Green taxis operate as dynamic point-to-point vehicles.
          Therefore, demand analytics and predictions are formulated around <strong>Pickup Geographic Zones</strong> (catchment clusters) rather than rigid routes.
        </p>
      </div>
    </div>
  );
};
