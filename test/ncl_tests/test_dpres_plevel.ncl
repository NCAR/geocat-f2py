begin
	plev = todouble((/ 1000,950,900,850,800,750,700,650,600,550,500,450,400,350,300,250,200,175,150,125,100, 80, 70, 60, 50,40, 30, 25, 20, 10 /))

	plev = plev * 100

	print(plev)

	ptop = min(plev)

	print(ptop)

	psfc = 101800.0

	print(psfc)

	iopt = 0

	dp = dpres_plevel(plev, psfc, ptop, iopt)

	print(dp)
end
