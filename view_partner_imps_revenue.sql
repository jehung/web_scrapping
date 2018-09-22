SELECT r.partner AS partner,CASE WHEN ss.name contains('thefirearmblog') THEN 'thefirearmblog.com/blog'
                             ELSE ss.name END AS site,
                            CASE WHEN INTEGER(s.profileid) = 114959274 THEN 6368387
                                 ELSE INTEGER(s.profileid) END AS profileid,
CASE
WHEN (r.vertical = '' OR s.xvertical = '')   THEN NULL
WHEN (s.xvertical IS NOT NULL AND s.xvertical != '') THEN s.xvertical
ELSE r.vertical END AS vertical,
r.site as partner_site_tag, r.revenue as revenue, r.imps as imps, r.date AS date FROM (
SELECT *
FROM  (SELECT SUM(earnings) AS revenue, FLOAT(SUM(imps)) as imps, 'a9' AS partner, date,
                REPLACE(REPLACE(lower(site),'http://',''),'www.','') as site FROM revenue.a9_l60d
                WHERE date > (SELECT MAX(date) FROM revenue.a9)
                GROUP BY partner, date, site
                ),
          (SELECT SUM(earnings) AS revenue, FLOAT(SUM(imps)) as imps, 'a9' AS partner, date,
                REPLACE(REPLACE(lower(site),'http://',''),'www.','') as site FROM revenue.a9
                GROUP BY partner, date, site
                ),
       (SELECT SUM(earnings) AS revenue, FLOAT(SUM(individual_ad_impressions)) as imps, 'adlogix' AS partner, date,
                REPLACE(REPLACE(lower(domain_name),'http://',''),'www.','') as site FROM revenue.adlogix_l60d
                WHERE date > (SELECT MAX(date) FROM revenue.adlogix)
                GROUP BY partner, date, site
                ),
          (SELECT SUM(earnings) AS revenue, FLOAT(SUM(individual_ad_impressions)) as imps, 'adlogix' AS partner, date,
                REPLACE(REPLACE(lower(domain_name),'http://',''),'www.','') as site FROM revenue.adlogix
                GROUP BY partner, date, site
                ),
      (SELECT SUM(earnings) AS revenue, FLOAT(SUM(individual_ad_impressions)) as imps, 'adsense' AS partner, date,
                REPLACE(REPLACE(lower(domain_name),'http://',''),'www.','') as site FROM revenue.adsense_l60d
                WHERE date > (SELECT MAX(date) FROM revenue.adsense)
                GROUP BY partner, date, site
                ),
          (SELECT SUM(earnings) AS revenue, FLOAT(SUM(individual_ad_impressions)) as imps, 'adsense' AS partner, date,
                REPLACE(REPLACE(lower(domain_name),'http://',''),'www.','') as site FROM revenue.adsense
                GROUP BY partner, date, site
                ),
        (SELECT SUM(earnings) AS revenue, FLOAT(SUM(individual_ad_impressions)) as imps, 'adsense' AS partner, date,
                REPLACE(REPLACE(lower(domain_name),'http://',''),'www.','') as site FROM fixya.adsense_l60d
                GROUP BY partner, date, site
                ),
        (SELECT SUM(earnings) AS revenue, FLOAT(SUM(individual_ad_impressions)) as imps, 'adsense' AS partner, date,
                REPLACE(REPLACE(lower(domain_name),'http://',''),'www.','') as site FROM fixya.adsense
                WHERE date < (SELECT MIN(date) FROM [fixya.adsense_l60d])
                GROUP BY partner, date, site
                ),
      (SELECT SUM(Revenue) AS revenue, FLOAT(SUM((revenue / eCPM)*1000)) as imps, 'adtech' AS partner, date,
                vertical FROM revenue.adtech_l60d
                WHERE date > (SELECT MAX(date) FROM revenue.adtech)
                GROUP BY partner, date, vertical
                ),
          (SELECT SUM(Revenue) AS revenue, FLOAT(SUM((revenue / eCPM)*1000)) as imps, 'adtech' AS partner, date,
                vertical FROM revenue.adtech
                GROUP BY partner, date, vertical
                ),
      (SELECT SUM(earnings) AS revenue, FLOAT(SUM(individual_ad_impressions)) as imps, 'adx' AS partner, date,
                REPLACE(REPLACE(REPLACE(lower(domain_name),'http://',''),'www.',''), ' (in app)', '') as site FROM revenue.adx_l60d
                WHERE date > (SELECT MAX(date) FROM revenue.adx) AND auction_type != 'PMP'
                GROUP BY partner, date, site
                ),
          (SELECT SUM(earnings) AS revenue, FLOAT(SUM(individual_ad_impressions)) as imps, 'adx' AS partner, date,
                REPLACE(REPLACE(REPLACE(lower(domain_name),'http://',''),'www.',''), ' (in app)', '') as site FROM revenue.adx
                WHERE auction_type != 'PMP'
                GROUP BY partner, date, site
                ),
        (SELECT SUM(revenue) AS revenue, FLOAT(SUM(impressions)) as imps, 'adx' AS partner, date,
                REPLACE(REPLACE(lower(site),'http://',''),'www.','') as site FROM fixya.adx_l60d
                GROUP BY partner, date, site
                ),
       (SELECT SUM(revenue) AS revenue, FLOAT(SUM(impressions)) as imps, 'adx' AS partner, date,
                REPLACE(REPLACE(lower(site),'http://',''),'www.','') as site FROM fixya.adx
                WHERE date < (SELECT MIN(date) FROM [fixya.adx_l60d])
                GROUP BY partner, date, site
                ),
      (SELECT SUM(rev) AS revenue, FLOAT(SUM(imps)) as imps, 'appnexus' AS partner,  date, vertical
                FROM revenue.appnexus_l60d
                WHERE date > (SELECT MAX(date) FROM revenue.appnexus)
                GROUP BY partner, date, vertical
                ),
          (SELECT SUM(rev) AS revenue, FLOAT(SUM(imps)) as imps, 'appnexus' AS partner,  date, vertical
                FROM revenue.appnexus
                GROUP BY partner, date, vertical
                ),
       (SELECT SUM(rev) AS revenue, FLOAT(SUM(imps)) as imps, site, 'appnexus' AS partner,  date, vertical
                FROM fixya.appnexus_l60d
                GROUP BY partner, date, vertical, site
                ),
       (SELECT SUM(rev) AS revenue, FLOAT(SUM(imps)) as imps, site, 'appnexus' AS partner,  date, vertical
                FROM fixya.appnexus
                WHERE date < (SELECT MIN(date) FROM [fixya.appnexus_l60d])
                GROUP BY partner, date, vertical, site
                ),
      (SELECT SUM(earnings) AS revenue, FLOAT(-1) as imps, 'amazon' AS partner, date_shipped AS date,
                REPLACE(lower(traccking_id),'www.','') as site FROM revenue.amazon_affiliate_l60d
                WHERE date_shipped > (SELECT MAX(date_shipped) FROM revenue.amazon_affiliate)
                GROUP BY partner, date, site
                ),
          (SELECT SUM(earnings) AS revenue, FLOAT(-1) as imps, 'amazon' AS partner, date_shipped AS date,
                REPLACE(lower(traccking_id),'www.','') as site FROM revenue.amazon_affiliate
                GROUP BY partner, date, site
                ),
      (SELECT SUM(revenue) AS revenue, FLOAT(SUM(imps)) as imps, 'brealtime' AS partner,  date, vertical
                FROM revenue.brealtime_l60d
                WHERE date > (SELECT MAX(date) FROM revenue.brealtime)
                GROUP BY partner, date, vertical
                ),
          (SELECT SUM(revenue) AS revenue, FLOAT(SUM(imps)) as imps, 'brealtime' AS partner,  date, vertical
                FROM revenue.brealtime
                GROUP BY partner, date, vertical
                ),
      (SELECT SUM(revenue) AS revenue, FLOAT(SUM(impressions)) as imps, 'criteo' AS partner,  date, vertical
                FROM revenue.criteo_l60d
                WHERE date > (SELECT MAX(date) FROM revenue.criteo)
                GROUP BY partner, date, vertical
                ),
          (SELECT SUM(revenue) AS revenue, FLOAT(SUM(impressions)) as imps, 'criteo' AS partner,  date, vertical
                FROM revenue.criteo
                GROUP BY partner, date, vertical
                ),
      (SELECT SUM(earnings) AS revenue, FLOAT(SUM((earnings / ecpm)*1000)) as imps, 'districtm' AS partner,  date,
                REPLACE(lower(domain),'www.','') as site FROM revenue.districtm_l60d
                WHERE date > (SELECT MAX(date) FROM revenue.districtm)
                GROUP BY partner, date, site
                ),
          (SELECT SUM(earnings) AS revenue, FLOAT(SUM((earnings / ecpm)*1000)) as imps, 'districtm' AS partner,  date,
                REPLACE(lower(domain),'www.','') as site FROM revenue.districtm
                GROUP BY partner, date, site
                ),
      (SELECT SUM(rev) AS revenue, FLOAT(SUM(imps)) as imps, 'distroscale' AS partner,  date, vertical,
                REPLACE(lower(site),'www.','') as site FROM revenue.distroscale_l60d
                WHERE date > (SELECT MAX(date) FROM revenue.distroscale)
                GROUP BY partner, date, site, vertical
                ),
          (SELECT SUM(rev) AS revenue, FLOAT(SUM(imps)) as imps, 'distroscale' AS partner,  date, vertical,
                REPLACE(lower(site),'www.','') as site FROM revenue.distroscale
                GROUP BY partner, date, site, vertical
                ),
        (SELECT SUM(earnings) AS revenue, FLOAT(SUM(ad_imps)) as imps, 'gumgum' AS partner,  date, y.vertical as vertical,
                y.name as site FROM revenue.gumgum a LEFT JOIN static.site y ON a.profileid = y.ga_profile_id
                WHERE date < (SELECT MIN(date) FROM [revenue.gumgum_l60d])
                GROUP BY partner, date, site, vertical
                ),
       (SELECT SUM(earnings) AS revenue, FLOAT(SUM(ad_imps)) as imps, 'gumgum' AS partner,  date, y.vertical as vertical,
                y.name as site FROM revenue.gumgum_l60d a LEFT JOIN static.site y ON a.profileid = y.ga_profile_id
                GROUP BY partner, date, site, vertical
                ),
       (SELECT SUM(partner_revenue) AS revenue,  FLOAT(SUM((partner_revenue / partner_eCPM)*1000)) as imps, 'havenhome' AS partner, date,
                  REPLACE(lower(ga_site),'www.','') as site FROM revenue.havenhome_l60d
                  WHERE date > (SELECT MAX(date) FROM revenue.havenhome)
                  GROUP BY partner, date, site
                  ),
  (SELECT SUM(partner_revenue) AS revenue, FLOAT(SUM((partner_revenue / partner_eCPM)*1000)) as imps, 'havenhome' AS partner, date,
                  REPLACE(lower(ga_site),'www.','') as site FROM revenue.havenhome
                  GROUP BY partner, date, site
                  ),
      (SELECT SUM(earnings) AS revenue, FLOAT(SUM(impressions)) as imps, 'indexexchange' AS partner,  date, CASE
        WHEN vertical contains ('Sports Sites') THEN 'Sports'
        WHEN vertical = 'PowerSports' THEN 'Powersports'
        WHEN vertical = 'Home & Garden' THEN 'Home Improvement Group'
        WHEN vertical = 'Tech' THEN 'Technology'
        WHEN vertical = 'Lifestyle' THEN 'Health & Wellness'
        ELSE vertical
       END as vertical ,
                REPLACE(lower(name),'www.','') as site FROM revenue.indexexchange_l60d
                WHERE date > (SELECT MAX(date) FROM revenue.indexexchange)
                GROUP BY partner, date, site, vertical
                ),
          (SELECT SUM(earnings) AS revenue, FLOAT(SUM(impressions)) as imps, 'indexexchange' AS partner,  date, CASE
        WHEN vertical contains ('Sports Sites') THEN 'Sports'
        WHEN vertical = 'PowerSports' THEN 'Powersports'
        WHEN vertical = 'Home & Garden' THEN 'Home Improvement Group'
        WHEN vertical = 'Tech' THEN 'Technology'
        WHEN vertical = 'Lifestyle' THEN 'Health & Wellness'
        ELSE vertical
       END as vertical,
                REPLACE(lower(name),'www.','') as site FROM revenue.indexexchange
                GROUP BY partner, date, site, vertical
                ),
      (SELECT SUM(revenue) AS revenue, FLOAT(SUM(impressions)) as imps, 'index_ebda' AS partner, date, vertical,
                REPLACE(REPLACE(lower(site),'http://',''),'www.','') as site FROM revenue.indexexchange_ebda_l60d
                WHERE date > (SELECT MAX(date) FROM [revenue.indexexchange_ebda])
                GROUP BY partner, date, site, vertical
                ),
      (SELECT SUM(revenue) AS revenue, FLOAT(SUM(impressions)) as imps, 'index_ebda' AS partner, date, vertical,
                REPLACE(REPLACE(lower(site),'http://',''),'www.','') as site FROM [revenue.indexexchange_ebda]
                GROUP BY partner, date, site, vertical
                ),
      (SELECT SUM(revenue) AS revenue, FLOAT(SUM(impressions)) as imps, 'nativo' AS partner,  date,
                REPLACE(lower(site),'www.','') as site FROM revenue.nativo_l60d
                WHERE date > (SELECT MAX(date) FROM revenue.nativo)
                GROUP BY partner, date, site
                ),
          (SELECT SUM(revenue) AS revenue, FLOAT(SUM(impressions)) as imps, 'nativo' AS partner,  date,
                REPLACE(lower(site),'www.','') as site FROM revenue.nativo
                GROUP BY partner, date, site
                ),
       (SELECT SUM(revenue) AS revenue, FLOAT(SUM(total_impressions)) as imps, 'openx' AS partner, date,
                REPLACE(lower(domain_name),'www.','') as site FROM revenue.openx_l60d
                WHERE date > (SELECT MAX(date) FROM revenue.openx)
                GROUP BY partner, date, site
                ),
          (SELECT SUM(revenue) AS revenue, FLOAT(SUM(total_impressions)) as imps, 'openx' AS partner,  date,
                REPLACE(lower(domain_name),'www.','') as site FROM revenue.openx
                GROUP BY partner, date, site
                ),
      (SELECT SUM(revenue) AS revenue, FLOAT(SUM(ad_requests)) as imps, 'netseer' AS partner,  date, vertical,
                REPLACE(lower(site),'www.','') as site FROM revenue.netseer_l60d
                WHERE date > (SELECT MAX(date) FROM revenue.netseer)
                GROUP BY partner, date, site, vertical
                ),
          (SELECT SUM(revenue) AS revenue, FLOAT(SUM(ad_requests)) as imps, 'netseer' AS partner,  date, vertical,
                REPLACE(lower(site),'www.','') as site FROM revenue.netseer
                GROUP BY partner, date, site, vertical
                ),
          (SELECT SUM(revenue) AS revenue, FLOAT(SUM(impressions)) as imps, 'openx_ebda' AS partner, date, vertical,
              REPLACE(REPLACE(lower(site),'http://',''),'www.','') as site FROM revenue.openx_ebda_l60d
              GROUP BY partner, date, site, vertical
              ),
       (SELECT SUM(revenue) AS revenue, FLOAT(SUM(impressions)) as imps, 'openx_ebda' AS partner, date, vertical,
              REPLACE(REPLACE(lower(site),'http://',''),'www.','') as site FROM revenue.openx_ebda
              WHERE date < (SELECT MIN(date) FROM [revenue.openx_ebda_l60d])
              GROUP BY partner, date, site, vertical
              ),
      (SELECT SUM(rev) AS revenue, FLOAT(SUM((rev / rpm)*1000)) as imps, 'powerinbox' AS partner,  date, vertical,
                REPLACE(lower(site),'www.','') as site FROM revenue.powerinbox_l60d
                WHERE date > (SELECT MAX(date) FROM revenue.powerinbox)
                GROUP BY partner, date, site, vertical
                ),
          (SELECT SUM(rev) AS revenue, FLOAT(SUM((rev / rpm)*1000)) as imps, 'powerinbox' AS partner,  date, vertical,
                REPLACE(lower(site),'www.','') as site FROM revenue.powerinbox
                GROUP BY partner, date, site, vertical
                ),
           (SELECT SUM(netRevenue) AS revenue, FLOAT(SUM(totalImpressions)) as imps, 'pulsepoint' AS partner,  date, vertical
                FROM revenue.pulsepoint_l60d
                WHERE date > (SELECT MAX(date) FROM revenue.pulsepoint)
                GROUP BY partner, date, vertical
                ),
          (SELECT SUM(netRevenue) AS revenue, FLOAT(SUM(totalImpressions)) as imps, 'pulsepoint' AS partner,  date, vertical
                FROM revenue.pulsepoint
                GROUP BY partner, date, vertical
                ),
      (SELECT SUM(revenue) AS revenue, FLOAT(SUM(widget_imps)) as imps, 'revcontent' AS partner,  date, vertical,
                REPLACE(lower(site),'www.','') as site FROM revenue.revcontent_l60d
                WHERE date > (SELECT MAX(date) FROM revenue.revcontent)
                GROUP BY partner, date, site, vertical
                ),
          (SELECT SUM(revenue) AS revenue, FLOAT(SUM(widget_imps)) as imps, 'revcontent' AS partner,  date, vertical,
                REPLACE(lower(site),'www.','') as site FROM revenue.revcontent
                GROUP BY partner, date, site, vertical
                ),
      (SELECT SUM(Prorated_Revenue) AS revenue, FLOAT(SUM(Prorated_NetworkImpressions)) as imps, 'rubicon' AS partner,  date, vertical,
                REPLACE(lower(site),'www.','') as site FROM revenue.rubicon_l60d
                GROUP BY partner, date, site, vertical
                ),
          (SELECT SUM(Prorated_Revenue) AS revenue, FLOAT(SUM(Prorated_NetworkImpressions)) as imps, 'rubicon' AS partner, date, vertical,
                REPLACE(lower(site),'www.','') as site FROM revenue.rubicon
                WHERE date < (SELECT MIN(date) FROM [revenue.rubicon_l60d])
                GROUP BY partner, date, site, vertical
                ),
       (SELECT SUM(Prorated_Revenue) AS revenue, FLOAT(SUM(Prorated_NetworkImpressions)) as imps, 'rubicon' AS partner, date, vertical,
                REPLACE(lower(site),'www.','') as site FROM fixya.rubicon_l60d
                GROUP BY partner, date, site, vertical
                ),
       (SELECT SUM(Prorated_Revenue) AS revenue, FLOAT(SUM(Prorated_NetworkImpressions)) as imps, 'rubicon' AS partner, date, vertical,
                REPLACE(lower(site),'www.','') as site FROM fixya.rubicon
                WHERE date < (SELECT MIN(date) FROM [fixya.rubicon_l60d])
                GROUP BY partner, date, site, vertical
                ),
      (SELECT SUM(revenue) AS revenue, FLOAT(SUM(imps)) as imps, 'sekindo' AS partner,  date, vertical,
                REPLACE(lower(domain),'www.','') as site FROM revenue.sekindo_l60d
                WHERE date > (SELECT MAX(date) FROM revenue.sekindo)
                GROUP BY partner, date, vertical, site
                ),
          (SELECT SUM(revenue) AS revenue, FLOAT(SUM(imps)) as imps, 'sekindo' AS partner,  date, vertical,
                REPLACE(lower(domain),'www.','') as site FROM revenue.sekindo
                GROUP BY partner, date, vertical, site
                ),
      (SELECT SUM(rev) AS revenue, FLOAT(SUM(imps)) as imps, 'solvemedia' AS partner,  date, vertical,
                REPLACE(lower(site),'www.','') as site FROM revenue.solvemedia_l60d
                WHERE date > (SELECT MAX(date) FROM revenue.solvemedia)
                GROUP BY partner, date, site, vertical
                ),
          (SELECT SUM(rev) AS revenue, FLOAT(SUM(imps)) as imps, 'solvemedia' AS partner,  date, vertical,
                REPLACE(lower(site),'www.','') as site FROM revenue.solvemedia
                GROUP BY partner, date, site, vertical
                ),
      (SELECT SUM(revenue) AS revenue, FLOAT(SUM(impressions)) as imps, 'sovrn_ebda' AS partner, date, vertical,
                REPLACE(REPLACE(lower(site),'http://',''),'www.','') as site FROM revenue.sovrn_ebda_l60d
                WHERE date > (SELECT MAX(date) FROM [revenue.sovrn_ebda])
                GROUP BY partner, date, site, vertical
                ),
      (SELECT SUM(revenue) AS revenue, FLOAT(SUM(impressions)) as imps, 'sovrn_ebda' AS partner, date, vertical,
                REPLACE(REPLACE(lower(site),'http://',''),'www.','') as site FROM [revenue.sovrn_ebda]
                GROUP BY partner, date, site, vertical
                ),
       (SELECT SUM(revenue) AS revenue, FLOAT(SUM(impressions)) as imps, 'rubicon_ebda' AS partner, date, vertical,
                REPLACE(REPLACE(lower(site),'http://',''),'www.','') as site FROM [revenue.rubicon_ebda_l60d]
                GROUP BY partner, date, site, vertical
                ),
      (SELECT SUM(revenue) AS revenue, FLOAT(SUM(impressions)) as imps, 'rubicon_ebda' AS partner, date, vertical,
                REPLACE(REPLACE(lower(site),'http://',''),'www.','') as site FROM [revenue.rubicon_ebda]
                WHERE date < (SELECT MIN(date) FROM revenue.rubicon_ebda_l60d)
                GROUP BY partner, date, site, vertical
                ),
      (SELECT SUM(ad_revenue) AS revenue, FLOAT(SUM((ad_revenue / ad_rpm)*1000)) as imps, 'taboola' AS partner,  date,
                CASE WHEN site !='' THEN REPLACE(lower(site),'www.','') ELSE lower(publisher) END AS site
                FROM revenue.taboola_l60d
                WHERE date > (SELECT MAX(date) FROM revenue.taboola) AND (placement = 'None' OR placement is null)
                GROUP BY partner, date, site
                ),
          (SELECT SUM(ad_revenue) AS revenue, FLOAT(SUM((ad_revenue / ad_rpm)*1000)) as imps, 'taboola' AS partner,  date,
                CASE WHEN site !='' THEN REPLACE(lower(site),'www.','') ELSE lower(publisher) END AS site
                FROM revenue.taboola
                WHERE (placement = 'None' OR placement is null)
                GROUP BY partner, date, site
                ),
      (SELECT SUM(revenue) AS revenue, FLOAT(-1) as imps, 'viglink' AS partner,  date, vertical,
                REPLACE(lower(site),'www.','') as site FROM revenue.viglink_l60d
                WHERE date > (SELECT MAX(date) FROM revenue.viglink)
                GROUP BY partner, date, site, vertical
                ),
          (SELECT SUM(revenue) AS revenue, FLOAT(-1) as imps, 'viglink' AS partner,  date, vertical,
                REPLACE(lower(site),'www.','') as site FROM revenue.viglink
                GROUP BY partner, date, site, vertical
                ),
     (SELECT SUM(revenue) AS revenue, FLOAT(SUM(imps)) as imps, partner, date,
                REPLACE(lower(site), 'www.', '') as site FROM [view.fitgroup_partner_revenue]
                GROUP BY partner, date, site),
    (SELECT SUM(revenue) AS revenue, FLOAT(SUM(imps)) as imps,
            CASE
              WHEN partner = 'adsense (for search)' THEN 'adsense'
              ELSE partner
            END as partner,date, 'varagesale.com' as site
            FROM ([varagesale.combined_revenues])
            GROUP BY partner, date, site),
    (SELECT SUM(amount) as revenue, FLOAT(-1) as imps, 'braintree' as partner, date,
            REPLACE(lower(domain_name), 'www.', '') as site FROM [revenue.braintree_l60d]
            WHERE date > (SELECT MAX(date) FROM revenue.braintree)
            GROUP BY partner, date, site),
      (SELECT SUM(amount) as revenue, FLOAT(-1) as imps, 'braintree' as partner, date,
            REPLACE(lower(domain_name), 'www.', '') as site FROM [revenue.braintree]
            GROUP BY partner, date, site),
     (SELECT SUM(Earnings) AS revenue, FLOAT(SUM(Impressions)) as imps, 'sovrn' AS partner,  date,
      lower(REPLACE(Site,'www.','')) AS site
            FROM [revenue.sovrn_l60d]
            GROUP BY partner, date, site),
      (SELECT SUM(revenue) AS revenue, FLOAT(SUM(impressions)) as imps, 'slimcut' AS partner, date, vertical,
                REPLACE(REPLACE(lower(site),'http://',''),'www.','') as site FROM revenue.slimcut_l60d
                WHERE date > (SELECT MAX(date) FROM [revenue.slimcut])
                GROUP BY partner, date, site, vertical
                ),
      (SELECT SUM(revenue) AS revenue, FLOAT(SUM(impressions)) as imps, 'slimcut' AS partner, date, vertical,
                REPLACE(REPLACE(lower(site),'http://',''),'www.','') as site FROM [revenue.slimcut]
                GROUP BY partner, date, site, vertical
                ),
        (SELECT SUM(commission) as revenue, FLOAT(-1) as imps, 'shareasale' as partner, date,
            REPLACE(lower(site), 'www.', '') as site FROM [revenue.shareasale_l60d]
            GROUP BY partner, date, site),
      (SELECT SUM(commission) as revenue, FLOAT(-1) as imps, 'shareasale' as partner, date,
            REPLACE(lower(site), 'www.', '') as site FROM [revenue.shareasale]
            WHERE date < (SELECT MIN(date) FROM revenue.shareasale_l60d)
            GROUP BY partner, date, site),
       (SELECT SUM(revenue) AS revenue, FLOAT(SUM(impressions)) as imps, 'index_ebda_app' AS partner, date, vertical,
                REPLACE(REPLACE(lower(site),'http://',''),'www.','') as site FROM [revenue.app_ebda_l60d]
                WHERE yield_partner = 'Index Exchange'
                GROUP BY partner, date, site, vertical
                ),
         (SELECT SUM(revenue) AS revenue, FLOAT(SUM(impressions)) as imps, 'index_ebda_app' AS partner, date, vertical,
                REPLACE(REPLACE(lower(site),'http://',''),'www.','') as site FROM [revenue.app_ebda]
                WHERE date < (SELECT MIN(date) FROM [revenue.app_ebda_l60d])
                      AND yield_partner = 'Index Exchange'
                GROUP BY partner, date, site, vertical
                ),
        (SELECT SUM(revenue) AS revenue, FLOAT(SUM(impressions)) as imps, 'rubicon_ebda_app' AS partner, date, vertical,
                REPLACE(REPLACE(lower(site),'http://',''),'www.','') as site FROM [revenue.app_ebda_l60d]
                WHERE yield_partner = 'Rubicon - EBDA'
                GROUP BY partner, date, site, vertical
                ),
         (SELECT SUM(revenue) AS revenue, FLOAT(SUM(impressions)) as imps, 'rubicon_ebda_app' AS partner, date, vertical,
                REPLACE(REPLACE(lower(site),'http://',''),'www.','') as site FROM [revenue.app_ebda]
                WHERE date < (SELECT MIN(date) FROM [revenue.app_ebda_l60d])
                      AND yield_partner = 'Rubicon - EBDA'
                GROUP BY partner, date, site, vertical
                ),
        (SELECT SUM(total_commission) AS revenue, FLOAT(-1) as imps, 'pepperjam' AS partner, date,
                REPLACE(REPLACE(REPLACE(lower(website),'www.',''), 'https://', ''), 'http://', '') AS site FROM revenue.pepperjam_l60d
                WHERE date > (SELECT MAX(date) FROM [revenue.pepperjam])
                GROUP BY partner, date, site
                ),
        (SELECT SUM(total_commission) AS revenue, FLOAT(-1) as imps, 'pepperjam' AS partner, date,
                        REPLACE(REPLACE(REPLACE(lower(website),'www.',''), 'https://', ''), 'http://', '') AS site FROM revenue.pepperjam
                        GROUP BY partner, date, site
                        ),
        (SELECT SUM(total_commission) AS revenue, FLOAT(-1) as imps, 'rakuten' AS partner, date,
                site FROM revenue.rakuten_l60d
                WHERE date > (SELECT MAX(date) FROM [revenue.rakuten])
                GROUP BY partner, date, site
                ),
      (SELECT SUM(total_commission) AS revenue, FLOAT(-1) as imps, 'rakuten' AS partner, date,
                      site FROM revenue.rakuten
                      GROUP BY partner, date, site
                      ),
      (SELECT SUM(commission) AS revenue, FLOAT(-1) as imps, 'performance horizon' AS partner, date,
                site FROM revenue.phg_l60d
                GROUP BY partner, date, site
                ),
      (SELECT SUM(total_cost) AS revenue, FLOAT(-1) as imps, 'impact radius' AS partner, date,
                site FROM revenue.impactradius_l60d
                WHERE date > (SELECT MAX(date) FROM [revenue.impactradius])
                GROUP BY partner, date, site
                ),
      (SELECT SUM(total_cost) AS revenue, FLOAT(-1) as imps, 'impact radius' AS partner, date,
                      site FROM revenue.impactradius
                      GROUP BY partner, date, site
                      ),
      (SELECT SUM(revenue) AS revenue, SUM(FLOAT(imps)) as imps, 'media.net' AS partner, date,
                site FROM fixya.medianet_l60d
                GROUP BY partner, date, site
                ),
       (SELECT SUM(revenue) AS revenue, SUM(FLOAT(imps)) as imps, 'media.net' AS partner, date,
                site FROM fixya.medianet
                WHERE date < (SELECT MIN(date) FROM [fixya.medianet_l60d])
                GROUP BY partner, date, site
                ),
      (select A.date_shipped as date, 'amazon uk affiliate' as partner, SUM(A.earnings / B.rate) as revenue,
            FLOAT(-1) as imps, 'unknown' as site
      from  (SELECT *
            FROM (revenue.amazon_uk_affiliate_l60d),
            (select * from [revenue.amazon_uk_affiliate]
             where date_shipped < (select min(date_shipped) from [revenue.amazon_uk_affiliate_l60d]))) A
            left join
            (select date, rate from [finance.forex] where symbol = 'USDEUR') B
            on A.date_shipped = B.date
      group by date, partner),
      (SELECT SUM(earnings) AS revenue, SUM(FLOAT(impressions)) as imps, 'sovrn' AS partner, date,
                site FROM fixya.sovrn
                GROUP BY partner, date, site
                ),
      (SELECT SUM(earnings) AS revenue, SUM(FLOAT(individual_ad_impressions)) as imps, 'adx - carbonmedia' AS partner, date,
                domain_name as site FROM carbon.adx
                GROUP BY partner, date, site
                ),
       (SELECT SUM(earnings) AS revenue, SUM(FLOAT(total_impressions)) as imps, 'openx - carbonmedia' AS partner, date,
                domain_name as site FROM carbon.openx
                GROUP BY partner, date, site
                ),
       (SELECT SUM(revenue) AS revenue, SUM(FLOAT(impressions)) as imps, 'spotx - carbonmedia' AS partner, date,
                site as site FROM carbon.spotx
                GROUP BY partner, date, site
                ),
       (SELECT SUM(commission) AS revenue, FLOAT(-1) as imps, 'chillipad' AS partner, date,
                site FROM revenue.chillipad_l60d
                WHERE date > (SELECT MAX(date) FROM [revenue.chillipad])
                GROUP BY partner, date, site
                ),
      (SELECT SUM(commission) AS revenue, FLOAT(-1) as imps, 'chillipad' AS partner, date,
                            site FROM revenue.chillipad
                            GROUP BY partner, date, site
                            ),
      (SELECT A.revenue / B.rate as revenue, FLOAT(-1) as imps, 'psi gate' as partner, A.date as date, A.site as site
      FROM
          (SELECT date, SUM(amount) as revenue, site
          FROM [revenue.psi_gate]
          WHERE result = 'Approved'
          GROUP BY date, site) A
        LEFT JOIN
          (SELECT date, rate
           FROM [finance.forex]
           WHERE symbol = 'USDCAD') B
        ON A.date = B.date),
    (SELECT SUM(commission) AS revenue, FLOAT(-1) as imps, 'slumbercloud' AS partner, date,
                site FROM revenue.slumberCloud_l60d
                WHERE date > (SELECT MAX(date) FROM [revenue.slumberCloud])
                GROUP BY partner, date, site
                ),
     (SELECT SUM(commission) AS revenue, FLOAT(-1) as imps, 'slumbercloud' AS partner, date,
                            site
       FROM revenue.slumberCloud
       GROUP BY partner, date, site
                 ),
    (SELECT SUM(earnings) AS revenue, FLOAT(-1) as imps, 'spindle' AS partner, date,
                site FROM revenue.spindle_l60d
                WHERE date > (SELECT MAX(date) FROM [revenue.spindle])
                GROUP BY partner, date, site
                 ),
    (SELECT SUM(earnings) AS revenue, FLOAT(-1) as imps, 'spindle' AS partner, date,
                site FROM revenue.spindle
                GROUP BY partner, date, site
                ),
    (SELECT SUM(earnings) AS revenue, FLOAT(-1) as imps, 'acousticsleep' AS partner, date,
                site FROM revenue.accousticsleep_l60d
                WHERE date > (SELECT MAX(date) FROM [revenue.accousticsleep])
                GROUP BY partner, date, site
                ),
    (SELECT SUM(earnings) AS revenue, FLOAT(-1) as imps, 'acousticsleep' AS partner, date,
                site FROM revenue.accousticsleep
                GROUP BY partner, date, site
                ),
     (SELECT SUM(commission_amount) as revenue, FLOAT(-1) as imps, 'commission junction (VS)' as partner, date, site
        FROM revenue.cj
        GROUP BY partner, date, site
                ),
     (select sum(Total_Commission) as revenue, sum(float(-1)) as imps, 'avantlink (VS)' as partner, date, Website as site
      from [revenue.avantlink]
      group by partner, date, site)
    WHERE revenue>0
)
r
LEFT JOIN (SELECT partner as xpartner, site as xsite, profileid, vertical as xvertical
          FROM static.partner_site_link) s ON s.xpartner = r.partner AND s.xsite = r.site
LEFT JOIN (SELECT name, FLOAT(ga_profile_id) AS profileid FROM static.site) ss ON s.profileid = ss.profileid
