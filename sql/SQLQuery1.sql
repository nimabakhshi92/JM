create table JanatolMava.dbo.Hadis(
	Had_ID  bigint not null,
	Had_Title nvarchar(200) null,
	MasoumID int null,
	Had_Narrators nvarchar(max) null,
	Had_Text nvarchar(max) not null,
	Boo_ID int null,
	Had_BookVolNo int null,
	Had_BookPageNo int null,
	Had_BookHadisNo int null,
	Had_InsertionDatetime datetime
	)

create table JanatolMava.dbo.HadisSubject(
	HadS_ID  bigint identity not null,
	Had_ID bigint not null,
	HadS_Subject nvarchar(100) not null
	)

create table JanatolMava.dbo.AyatInHadis(
	AyaIH_ID  bigint identity not null,
	Had_ID bigint not null,
	AyaIH_SooreName nvarchar(100) not null,
	AyaIH_AyeNo int not null,
	)

create table JanatolMava.dbo.RelatedExplanation(
	RelE_ID  bigint identity not null,
	Had_ID bigint not null,
	RelE_Expression nvarchar(max) not null,
	RelE_Explanation nvarchar(max) not null,
)


create table JanatolMava.dbo.HadisSummaryInFehrest(
	HadSIF_ID  bigint identity not null,
	Had_ID bigint not null,
	HadSIF_Alphabet nvarchar(10) not null,
	HadSIF_subject nvarchar(100) not null,
	HadSIF_Summary nvarchar(max) null,
	HadSIF_InsertionDatetime datetime
	)

create table JanatolMava.dbo.AyatSummaryInFehrest(
	AyaSIF_ID  bigint identity not null,
	Had_ID bigint not null,
	AyaSIF_Alphabet nvarchar(10) not null,
	AyaSIF_Subject nvarchar(100) not null,
	AyaSIF_AyeExpression nvarchar(max) not null,
	AyaSIF_AyeExplanation nvarchar(max) not null,
	AyaSIF_InsertionDatetime datetime
)


create table JanatolMava.dbo.Masoum(
	MasoumID  int not null,
	MasoumName nvarchar(200) null,
	)
	'حضرت پیامبر صلی الله علیه و آله'
'حضرت امیرالمومنین علیه السلام'
'حضرت زهرا سلام الله علیها'
'امام حسن علیه السلام'
'امام حسین علیه السلام'
'امام سجاد علیه السلام'
'امام باقر علیه السلام'
'امام صادق علیه السلام'
'امام کاظم علیه السلام'
'امام رضا علیه السلام'
'امام جواد علیه السلام'
'امام هادی علیه السلام'
'امام حسن عسکری علیه السلام'
'امام زمان علیه السلام'
insert into JanatolMava.dbo.Masoum values(15, N'نامشخص')

select * from JanatolMava.dbo.Masoum


--drop table JanatolMava.dbo.Hadis
